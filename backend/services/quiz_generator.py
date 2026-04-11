from __future__ import annotations

from typing import Any

from services.gemini_service import GeminiService


class QuizGenerator:
    def __init__(self, gemini_service: GeminiService) -> None:
        self.gemini_service = gemini_service

    def generate(self, document_text: str) -> list[dict[str, Any]]:
        return self.gemini_service.generate_quiz(document_text)
