from __future__ import annotations

import asyncio
from dataclasses import dataclass

from services.gemini_service import GeminiService, GeminiServiceError
from services.vector_store import VectorStore, VectorStoreError


@dataclass
class KnowledgePack:
    summary: str
    concepts: list[dict[str, str]]
    definitions: list[str]
    teaching_context: str


class KnowledgeAgentError(Exception):
    pass


class KnowledgeAgent:
    def __init__(self, gemini: GeminiService, vector_store: VectorStore) -> None:
        self.gemini = gemini
        self.vector_store = vector_store

    async def build_document_knowledge(self, document_text: str) -> KnowledgePack:
        if not document_text.strip():
            raise KnowledgeAgentError("Document text is empty.")

        try:
            summary = await asyncio.to_thread(self.gemini.generate_summary, document_text)
            concepts = await asyncio.to_thread(self.gemini.generate_concepts, summary)
            defs_raw = await asyncio.to_thread(
                self.gemini.tutor_chat,
                "You are the Knowledge Agent. Extract important definitions from this summary as short bullet points.\n\n"
                f"Summary:\n{summary}",
            )
            definitions = [line.strip("-• ").strip() for line in defs_raw.splitlines() if line.strip()][:6]
            teaching_context = f"Summary:\n{summary}\n\nConcepts:\n{concepts}\n\nDefinitions:\n{definitions}"
            return KnowledgePack(
                summary=summary,
                concepts=concepts,
                definitions=definitions,
                teaching_context=teaching_context,
            )
        except GeminiServiceError as ex:
            raise KnowledgeAgentError(str(ex)) from ex
        except Exception as ex:
            raise KnowledgeAgentError(f"Knowledge extraction failed: {ex}") from ex

    async def retrieve_context(self, question: str, fallback_text: str) -> str:
        if not question.strip():
            return fallback_text[:4000]
        try:
            chunks = await asyncio.to_thread(self.vector_store.search_similar_chunks, question, 5)
            if not chunks:
                return fallback_text[:4000]
            return "\n\n".join(c.content for c in chunks)[:6000]
        except VectorStoreError:
            return fallback_text[:4000]
