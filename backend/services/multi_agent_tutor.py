from __future__ import annotations

from dataclasses import dataclass

from services.command_agent import CommandAgent
from services.evaluation_agent import EvaluationAgent, EvaluationAgentError
from services.knowledge_agent import KnowledgeAgent, KnowledgeAgentError
from services.tutor_agent import TutorAgent, TutorAgentError, TutorState
from services.voice_agent import VoiceAgent, VoiceAgentError


class MultiAgentTutorError(Exception):
    pass


@dataclass
class MultiAgentSession:
    wake_active: bool = False
    last_question: str = ""
    difficulty: str = "easy"


class MultiAgentTutor:
    def __init__(
        self,
        command_agent: CommandAgent,
        knowledge_agent: KnowledgeAgent,
        tutor_agent: TutorAgent,
        evaluation_agent: EvaluationAgent,
        voice_agent: VoiceAgent,
    ) -> None:
        self.command_agent = command_agent
        self.knowledge_agent = knowledge_agent
        self.tutor_agent = tutor_agent
        self.evaluation_agent = evaluation_agent
        self.voice_agent = voice_agent

    async def handle(
        self,
        session: MultiAgentSession,
        user_text: str,
        document_text: str,
        student_answer: str = "",
    ) -> dict:
        decision = self.command_agent.decide(user_text)
        trace = ["Command Agent"]

        if decision.action == "WAKE":
            session.wake_active = True
            return {
                "action": "WAKE",
                "response": "Yes, how can I help you?",
                "agent_trace": trace,
                "wake_active": True,
            }

        if decision.requires_wake_word and not session.wake_active:
            return {
                "action": "WAIT_WAKE",
                "response": "Say Jarvis, NeuroLearn, or Hey Tutor to activate me.",
                "agent_trace": trace,
                "wake_active": False,
            }

        if decision.requires_document and not document_text.strip():
            return {
                "action": decision.action,
                "response": "Please upload and analyze a document first.",
                "agent_trace": trace,
                "wake_active": True,
            }

        try:
            trace.append("Knowledge Agent")
            knowledge = await self.knowledge_agent.build_document_knowledge(document_text)

            trace.append("Tutor Agent")
            tutor_state = TutorState(difficulty=session.difficulty, last_question=session.last_question)
            tutor_turn = await self.tutor_agent.tutor_turn(
                question=user_text if user_text.strip() else "Explain the document",
                context=knowledge.teaching_context,
                state=tutor_state,
                student_answer=student_answer,
            )

            response = str(tutor_turn["response"])
            question = str(tutor_turn["question"])

            if student_answer.strip() and session.last_question:
                trace.append("Evaluation Agent")
                eval_result = await self.evaluation_agent.evaluate(session.last_question, student_answer, session.difficulty)
                response = f"{eval_result.feedback}\n\n{response}"
                session.difficulty = eval_result.next_difficulty
            else:
                session.difficulty = str(tutor_turn.get("difficulty", session.difficulty))

            session.last_question = question

            trace.append("Voice Agent")
            try:
                audio = await self.voice_agent.synthesize(response)
            except VoiceAgentError:
                audio = b""

            return {
                "action": decision.action,
                "response": response,
                "question": question,
                "difficulty": session.difficulty,
                "audio": audio,
                "agent_trace": trace,
                "wake_active": True,
            }
        except (KnowledgeAgentError, TutorAgentError, EvaluationAgentError) as ex:
            raise MultiAgentTutorError(str(ex)) from ex
        except Exception as ex:
            raise MultiAgentTutorError(f"Multi-agent handling failed: {ex}") from ex
