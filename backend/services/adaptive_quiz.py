from __future__ import annotations

from dataclasses import dataclass

from services.gemini_service import GeminiService, GeminiServiceError


@dataclass
class AdaptiveQuestion:
    difficulty: str
    question: str
    expected_answer: str


@dataclass
class AnswerEvaluation:
    is_correct: bool
    feedback: str


class AdaptiveQuizError(Exception):
    pass


class AdaptiveQuiz:
    LEVELS = ["easy", "medium", "hard"]

    def __init__(self, gemini: GeminiService) -> None:
        self.gemini = gemini

    def generate_question(self, context: str, difficulty: str = "easy") -> AdaptiveQuestion:
        level = self._normalize_difficulty(difficulty)
        prompt = (
            "You are an AI tutor creating one adaptive comprehension question. "
            f"Difficulty: {level}. "
            "Return exactly two lines:\n"
            "Question: <question text>\n"
            "ExpectedAnswer: <short answer>\n\n"
            f"Context:\n{context[:6000]}"
        )

        try:
            raw = self.gemini.tutor_chat(prompt, context=context[:4000]).strip()
            question, expected = self._parse_question_response(raw)
            return AdaptiveQuestion(difficulty=level, question=question, expected_answer=expected)
        except (GeminiServiceError, ValueError) as ex:
            raise AdaptiveQuizError(str(ex)) from ex

    def evaluate_answer(self, question: str, answer: str, expected_answer: str) -> AnswerEvaluation:
        if not answer.strip():
            return AnswerEvaluation(is_correct=False, feedback="I did not catch an answer. Please try again.")

        prompt = (
            "Evaluate a student's answer to a tutor question.\n"
            f"Question: {question}\n"
            f"Expected answer: {expected_answer}\n"
            f"Student answer: {answer}\n"
            "Return exactly:\n"
            "Result: correct or incorrect\n"
            "Feedback: <short supportive feedback>"
        )

        try:
            raw = self.gemini.tutor_chat(prompt).strip().lower()
            is_correct = "result: correct" in raw
            feedback_line = next((line for line in raw.splitlines() if line.startswith("feedback:")), "feedback: good try")
            feedback = feedback_line.replace("feedback:", "").strip().capitalize()
            return AnswerEvaluation(is_correct=is_correct, feedback=feedback)
        except GeminiServiceError as ex:
            raise AdaptiveQuizError(str(ex)) from ex

    def next_difficulty(self, previous_result: bool, current: str) -> str:
        level = self._normalize_difficulty(current)
        idx = self.LEVELS.index(level)

        if previous_result and idx < len(self.LEVELS) - 1:
            return self.LEVELS[idx + 1]
        if not previous_result and idx > 0:
            return self.LEVELS[idx - 1]
        return level

    def _normalize_difficulty(self, difficulty: str) -> str:
        value = (difficulty or "easy").strip().lower()
        if value not in self.LEVELS:
            return "easy"
        return value

    def _parse_question_response(self, raw: str) -> tuple[str, str]:
        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        q_line = next((line for line in lines if line.lower().startswith("question:")), "")
        a_line = next((line for line in lines if line.lower().startswith("expectedanswer:")), "")

        if not q_line or not a_line:
            raise ValueError("Adaptive question response format invalid.")

        question = q_line.split(":", 1)[1].strip()
        expected = a_line.split(":", 1)[1].strip()
        if not question or not expected:
            raise ValueError("Adaptive question or expected answer empty.")
        return question, expected
