from __future__ import annotations

from services.gemini_service import GeminiService
from services.vector_store import VectorStore


class RAGService:
    def __init__(self, vector_store: VectorStore, gemini_service: GeminiService) -> None:
        self.vector_store = vector_store
        self.gemini_service = gemini_service

    def answer_question(self, question: str, k: int = 5) -> dict:
        relevant_chunks = self.vector_store.search_similar_chunks(question, k=k)
        context = "\n\n".join(
            f"[Page {chunk.page_number} | {chunk.section}] {chunk.content}" for chunk in relevant_chunks
        )

        answer = self.gemini_service.tutor_chat(question=question, context=context)
        return {
            "answer": answer,
            "sources": [chunk.model_dump() for chunk in relevant_chunks],
        }
