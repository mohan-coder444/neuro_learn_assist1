from __future__ import annotations

import json
import logging
import os
import threading
from pathlib import Path

import faiss
import google.generativeai as genai
import numpy as np

from models.document_model import DocumentChunk

logger = logging.getLogger(__name__)


class VectorStoreError(Exception):
    pass


class VectorStore:
    def __init__(self, storage_dir: str = "data") -> None:
        self.storage = Path(storage_dir)
        self.storage.mkdir(parents=True, exist_ok=True)

        self.index_path = self.storage / "faiss.index"
        self.meta_path = self.storage / "chunks.json"

        self.index: faiss.IndexFlatL2 | None = None
        self.chunks: list[DocumentChunk] = []
        self.embedding_dim = 768
        self.embedding_model_candidates = [
            "models/embedding-001",
            "models/gemini-embedding-001",
            "models/gemini-embedding-2-preview",
        ]
        self.embedding_model = "models/embedding-001"
        self.available_embedding_models: list[str] = []
        self._lock = threading.Lock()

        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY is not set. Embedding calls will fail.")
        else:
            if not os.getenv("GOOGLE_API_KEY"):
                os.environ["GOOGLE_API_KEY"] = api_key
            genai.configure(api_key=api_key)
            self._discover_embedding_model()

        self._load_if_exists()

    def create_embeddings(self, texts: list[str], is_query: bool = False) -> np.ndarray:
        if not texts:
            raise VectorStoreError("No text provided to create embeddings.")

        task_type = "retrieval_query" if is_query else "retrieval_document"
        try:
            vectors: list[list[float]] = []
            for text in texts:
                embedding = self._embed_with_fallback(text=text, task_type=task_type)
                vectors.append(embedding)
        except Exception as ex:
            raise VectorStoreError(f"Embedding generation failed: {ex}") from ex

        arr = np.array(vectors, dtype="float32")
        if arr.ndim != 2:
            raise VectorStoreError("Embedding output has invalid shape.")

        self.embedding_dim = arr.shape[1]
        return arr

    def store_embeddings(self, chunks: list[DocumentChunk]) -> None:
        if not chunks:
            raise VectorStoreError("No chunks provided for storage.")

        with self._lock:
            self.chunks = chunks
            embeddings = self.create_embeddings([c.content for c in chunks], is_query=False)

            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self.index.add(embeddings)

            faiss.write_index(self.index, str(self.index_path))
            self.meta_path.write_text(
                json.dumps([c.model_dump() for c in chunks], ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

    def store_embeddings_background(self, chunks_payload: list[dict] | list[DocumentChunk]) -> None:
        chunks: list[DocumentChunk] = []
        for item in chunks_payload:
            if isinstance(item, DocumentChunk):
                chunks.append(item)
            else:
                chunks.append(DocumentChunk(**item))
        self.store_embeddings(chunks)

    def search_similar_chunks(self, query: str, k: int = 5) -> list[DocumentChunk]:
        if not query.strip():
            raise VectorStoreError("Query cannot be empty.")
        if self.index is None:
            raise VectorStoreError("Vector index is not initialized.")

        query_vec = self.create_embeddings([query], is_query=True)
        k = min(k, len(self.chunks))
        if k <= 0:
            return []

        distances, indices = self.index.search(query_vec, k)
        _ = distances

        results: list[DocumentChunk] = []
        for idx in indices[0]:
            if 0 <= idx < len(self.chunks):
                results.append(self.chunks[idx])
        return results

    def _load_if_exists(self) -> None:
        if self.index_path.exists() and self.meta_path.exists():
            try:
                self.index = faiss.read_index(str(self.index_path))
                meta = json.loads(self.meta_path.read_text(encoding="utf-8"))
                self.chunks = [DocumentChunk(**m) for m in meta]
                if self.index.d > 0:
                    self.embedding_dim = self.index.d
            except Exception as ex:
                logger.warning("Failed to load FAISS index metadata: %s", ex)
                self.index = None
                self.chunks = []

    def _embed_with_fallback(self, text: str, task_type: str) -> list[float]:
        ordered_models = [self.embedding_model]
        ordered_models.extend(m for m in self.embedding_model_candidates if m not in ordered_models)
        ordered_models.extend(m for m in self.available_embedding_models if m not in ordered_models)

        last_error: Exception | None = None
        for model_name in ordered_models:
            try:
                response = genai.embed_content(
                    model=model_name,
                    content=text,
                    task_type=task_type,
                )
                embedding = response.get("embedding")
                if not embedding:
                    raise VectorStoreError("Empty embedding returned by Gemini.")
                if self.embedding_model != model_name:
                    logger.info("Switched embedding model from %s to %s", self.embedding_model, model_name)
                    self.embedding_model = model_name
                return embedding
            except Exception as ex:
                last_error = ex
                continue

        # Final retry after refreshing model discovery list.
        self._discover_embedding_model()
        if self.embedding_model not in ordered_models:
            response = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type=task_type,
            )
            embedding = response.get("embedding")
            if not embedding:
                raise VectorStoreError("Empty embedding returned by Gemini.")
            return embedding

        raise VectorStoreError(f"No usable embedding model found. Last error: {last_error}")

    def _discover_embedding_model(self) -> None:
        try:
            discovered: list[str] = []
            for model in genai.list_models():
                name = getattr(model, "name", "")
                methods = getattr(model, "supported_generation_methods", []) or []
                if name and "embedContent" in methods:
                    discovered.append(name)

            self.available_embedding_models = discovered
            if not discovered:
                return

            for preferred in self.embedding_model_candidates:
                if preferred in discovered:
                    self.embedding_model = preferred
                    logger.info("Discovered preferred embedding model: %s", preferred)
                    return

            self.embedding_model = discovered[0]
            logger.info("Discovered embedding model fallback: %s", self.embedding_model)
        except Exception as ex:
            logger.warning("Could not discover Gemini embedding models: %s", ex)
