from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import AsyncGenerator

from services.adaptive_quiz import AdaptiveQuiz, AdaptiveQuizError
from services.emotion_detector import EmotionDetector
from services.gemini_service import GeminiService, GeminiServiceError
from services.voice_pipeline import VoicePipeline, VoicePipelineError
from services.voice_streamer import VoiceStreamer, VoiceStreamerError


class TutorAgentError(Exception):
    pass


@dataclass
class TutorState:
    difficulty: str = "easy"
    last_question: str = ""
    expected_answer: str = ""


class TutorAgent:
    def __init__(
        self,
        gemini: GeminiService,
        voice_pipeline: VoicePipeline,
        adaptive_quiz: AdaptiveQuiz,
        emotion_detector: EmotionDetector,
        voice_streamer: VoiceStreamer | None = None,
    ) -> None:
        self.gemini = gemini
        self.voice_pipeline = voice_pipeline
        self.adaptive_quiz = adaptive_quiz
        self.emotion_detector = emotion_detector
        self.voice_streamer = voice_streamer

    async def tutor_turn(self, question: str, context: str, state: TutorState, student_answer: str = "") -> dict[str, str | bool]:
        if not question.strip() and not student_answer.strip():
            raise TutorAgentError("Tutor turn requires a question or student answer.")

        try:
            emotion = self.emotion_detector.detect(student_answer)

            explain_prompt = (
                "You are an AI tutor teaching a student about a document. "
                "Explain clearly, then ask a question. "
                "If the student answers correctly, increase difficulty. "
                "If incorrect, simplify explanation.\n\n"
                f"Current difficulty: {state.difficulty}\n"
                f"Student question: {question}\n"
                f"Student answer: {student_answer}\n"
                f"Context:\n{context[:8000]}"
            )

            explanation = await asyncio.to_thread(self.gemini.tutor_chat, explain_prompt, context)
            explanation = explanation.strip()
            if not explanation:
                raise TutorAgentError("Tutor generated an empty explanation.")

            adaptive_q = await asyncio.to_thread(self.adaptive_quiz.generate_question, context, state.difficulty)
            feedback = ""
            is_correct = False

            if student_answer.strip() and state.last_question:
                eval_result = await asyncio.to_thread(
                    self.adaptive_quiz.evaluate_answer,
                    state.last_question,
                    student_answer,
                    state.expected_answer,
                )
                is_correct = eval_result.is_correct
                feedback = eval_result.feedback
                state.difficulty = await asyncio.to_thread(self.adaptive_quiz.next_difficulty, is_correct, state.difficulty)
            elif student_answer.strip():
                feedback = "Thanks for your answer. I will ask a focused question now."

            if emotion.is_confused:
                feedback = f"{emotion.encouragement} {feedback}".strip()

            state.last_question = adaptive_q.question
            state.expected_answer = adaptive_q.expected_answer

            response_text = (
                f"{explanation}\n\n"
                f"{feedback}\n"
                f"Question ({state.difficulty.title()}): {adaptive_q.question}"
            ).strip()

            return {
                "response": response_text,
                "question": adaptive_q.question,
                "difficulty": state.difficulty,
                "feedback": feedback,
                "is_correct": is_correct,
                "tone": emotion.tone,
            }
        except (GeminiServiceError, AdaptiveQuizError) as ex:
            raise TutorAgentError(str(ex)) from ex
        except Exception as ex:
            raise TutorAgentError(f"Tutor turn failed: {ex}") from ex

    async def tutor_conversation(self, question: str, context: str) -> dict[str, str | bytes]:
        if not question.strip():
            raise TutorAgentError("Question is empty.")

        prompt = (
            "You are an AI tutor teaching a student about a document. "
            "Explain clearly, then ask a question. "
            "If the student answers correctly, increase difficulty. "
            "If incorrect, simplify explanation.\n\n"
            f"Document context:\n{context[:8000]}\n\n"
            f"Student question:\n{question}"
        )

        try:
            response_text = await asyncio.to_thread(self.gemini.tutor_chat, prompt, context)
            response_text = response_text.strip()
            if not response_text:
                raise TutorAgentError("Tutor response is empty.")
            speech_audio = await asyncio.to_thread(self.voice_pipeline.synthesize_tutor_audio, response_text)
            return {
                "response": response_text,
                "audio": speech_audio,
            }
        except (GeminiServiceError, VoicePipelineError) as ex:
            raise TutorAgentError(str(ex)) from ex
        except Exception as ex:
            raise TutorAgentError(f"Tutor conversation failed: {ex}") from ex

    async def tutor_conversation_stream(self, question: str, context: str) -> AsyncGenerator[dict[str, str], None]:
        if not question.strip():
            raise TutorAgentError("Question is empty.")
        if self.voice_streamer is None:
            raise TutorAgentError("Voice streamer is not configured.")

        prompt = (
            "You are an ultra-fast AI tutor. Respond in concise educational chunks. "
            "Teach clearly and ask one follow-up question at the end.\n\n"
            f"Context:\n{context[:8000]}\n\n"
            f"Question:\n{question}"
        )

        try:
            index = 0
            async for chunk_text in self.voice_streamer.stream_text(prompt):
                yield {"index": str(index), "text": chunk_text}
                index += 1
        except (GeminiServiceError, VoiceStreamerError) as ex:
            raise TutorAgentError(str(ex)) from ex
        except Exception as ex:
            raise TutorAgentError(f"Tutor streaming failed: {ex}") from ex
