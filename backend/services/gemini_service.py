from __future__ import annotations

import json
import logging
import os
from typing import Any

import google.generativeai as genai

logger = logging.getLogger(__name__)


class GeminiServiceError(Exception):
    pass


class GeminiService:
    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY is not set.")
        else:
            genai.configure(api_key=api_key)

        self.model_candidates = [
            os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
            "gemini-1.5-flash-latest",
            "gemini-2.0-flash",
            "gemini-2.5-flash",
        ]
        self.model = genai.GenerativeModel(self.model_candidates[0])

    def generate_summary(self, document_text: str) -> str:
        prompt = (
            "Summarize the following educational document in a concise, accessible way. "
            "Use headings and bullet points where helpful.\n\n"
            f"DOCUMENT:\n{document_text}"
        )
        return self._generate_text(prompt)

    def generate_concepts(self, document_text: str) -> list[dict[str, str]]:
        prompt = (
            "Extract the key concepts from this document. "
            "Return JSON array only, each object with: concept, explanation.\n\n"
            f"DOCUMENT:\n{document_text}"
        )
        return self._generate_json(prompt)

    # Backward compatibility alias
    def generate_key_concepts(self, document_text: str) -> list[dict[str, str]]:
        return self.generate_concepts(document_text)

    def generate_flashcards(self, document_text: str) -> list[dict[str, str]]:
        prompt = (
            "Create study flashcards from the document. "
            "Return JSON array only, each object must contain: question, answer.\n\n"
            f"DOCUMENT:\n{document_text}"
        )
        return self._generate_json(prompt)

    def generate_quiz(self, document_text: str) -> list[dict[str, Any]]:
        prompt = (
            "Generate exactly 5 MCQ questions from this document. "
            "Return JSON array only. Each object must include: "
            "question, options (array of 4 choices), correct_answer, explanation.\n\n"
            f"DOCUMENT:\n{document_text}"
        )
        return self._generate_json(prompt)

    def tutor_chat(self, question: str, context: str = "") -> str:
        prompt = (
            "You are a friendly AI teacher explaining concepts clearly to students. "
            "Explain like a teacher guiding a student. "
            "Give examples and end with one follow-up question.\n\n"
            f"CONTEXT:\n{context}\n\n"
            f"STUDENT QUESTION:\n{question}"
        )
        return self._generate_text(prompt)

    # Backward compatibility alias
    def chat_with_document(self, question: str, context: str) -> str:
        return self.tutor_chat(question, context)

    def _generate_text(self, prompt: str) -> str:
        last_error: Exception | None = None

        for model_name in self.model_candidates:
            try:
                response = genai.GenerativeModel(model_name).generate_content(prompt)
                if not response.text:
                    raise GeminiServiceError("Empty response from Gemini.")
                self.model = genai.GenerativeModel(model_name)
                return response.text.strip()
            except Exception as ex:
                last_error = ex
                continue

        raise GeminiServiceError(f"Gemini generation failed: {last_error}")

    def _generate_json(self, prompt: str) -> list[dict[str, Any]]:
        response_text = self._generate_text(prompt)

        cleaned = response_text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            cleaned = cleaned.replace("json", "", 1).strip()

        try:
            parsed = json.loads(cleaned)
            if not isinstance(parsed, list):
                raise GeminiServiceError("Gemini did not return a JSON array.")
            return parsed
        except json.JSONDecodeError:
            # Retry once with strong formatting instruction
            repair_prompt = (
                "Convert the following content to valid JSON array only. "
                "Do not include markdown.\n\n"
                f"CONTENT:\n{response_text}"
            )
            repaired = self._generate_text(repair_prompt)
            repaired = repaired.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            try:
                parsed = json.loads(repaired)
                if not isinstance(parsed, list):
                    raise GeminiServiceError("Repaired output is not a JSON array.")
                return parsed
            except Exception as ex:
                raise GeminiServiceError(f"Failed to parse Gemini JSON output: {ex}") from ex
