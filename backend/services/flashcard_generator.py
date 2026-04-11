from __future__ import annotations

from services.gemini_service import GeminiService


class FlashcardGenerator:
    def __init__(self, gemini_service: GeminiService) -> None:
        self.gemini_service = gemini_service

    def generate(self, document_text: str) -> list[dict[str, str]]:
        return self.gemini_service.generate_flashcards(document_text)
