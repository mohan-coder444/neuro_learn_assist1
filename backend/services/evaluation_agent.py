from __future__ import annotations

import asyncio
from dataclasses import dataclass

from services.gemini_service import GeminiService, GeminiServiceError


@dataclass
class EvaluationResult:
    is_correct: bool
    feedback: str
    next_difficulty: str


class EvaluationAgentError(Exception):
    pass


class EvaluationAgent:
    def __init__(self, gemini: GeminiService) -> None:
        self.gemini = gemini

    async def evaluate(self, question: str, student_answer: str, difficulty: str) -> EvaluationResult:
        if not student_answer.strip():
            return EvaluationResult(
                is_correct=False,
                feedback="I could not hear an answer. Let's try one more time, step by step.",
                next_difficulty=max(difficulty, "easy"),
            )

        prompt = (
            "You are the Evaluation Agent. Evaluate the student's answer.\n"
            f"Question: {question}\n"
            f"Student answer: {student_answer}\n"
            "Return exactly two lines:\n"
            "Result: correct or incorrect\n"
            "Feedback: <supportive feedback>"
        )

        try:
            result = await asyncio.to_thread(self.gemini.tutor_chat, prompt)
            normalized = result.lower()
            is_correct = "result: correct" in normalized
            feedback_line = next((line for line in result.splitlines() if line.lower().startswith("feedback:")), "Feedback: Good effort.")
            feedback = feedback_line.split(":", 1)[1].strip()
            next_difficulty = self._next_difficulty(is_correct, difficulty)
            if not is_correct:
                feedback = f"{feedback} Let's simplify it and try again."
            return EvaluationResult(is_correct=is_correct, feedback=feedback, next_difficulty=next_difficulty)
        except GeminiServiceError as ex:
            raise EvaluationAgentError(str(ex)) from ex
        except Exception as ex:
            raise EvaluationAgentError(f"Evaluation failed: {ex}") from ex

    def _next_difficulty(self, correct: bool, current: str) -> str:
        levels = ["easy", "medium", "hard"]
        current = current if current in levels else "easy"
        idx = levels.index(current)
        if correct and idx < len(levels) - 1:
            return levels[idx + 1]
        if not correct and idx > 0:
            return levels[idx - 1]
        return current
