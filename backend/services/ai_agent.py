from __future__ import annotations

from dataclasses import dataclass

from services.command_parser import detect_intent, parse_voice_command


@dataclass
class AgentReply:
    intent: str
    action: str
    response: str
    requires_wake_word: bool = False


class NeuroLearnAgent:
    def __init__(self) -> None:
        self.active_session = False

    def handle_command(self, text: str) -> AgentReply:
        normalized = (text or "").strip()
        if not normalized:
            return AgentReply(intent="CHAT", action="UNKNOWN", response="I did not catch that. Please repeat.")

        parsed = parse_voice_command(normalized)

        if parsed.action == "WAKE":
            self.active_session = True
            return AgentReply(
                intent="WAKE",
                action="WAKE",
                response="Yes, how can I help you?",
            )

        if not self.active_session and parsed.requires_wake_word:
            return AgentReply(
                intent="SLEEP",
                action="WAIT_WAKE",
                response="Say Jarvis, NeuroLearn, or Hey Tutor to activate me.",
                requires_wake_word=True,
            )

        intent = detect_intent(normalized)

        if intent == "UPLOAD":
            return AgentReply(intent=intent, action="UPLOAD", response="Sure. Uploading the document now.")
        if intent == "EXPLAIN":
            return AgentReply(intent=intent, action="EXPLAIN", response="Understood. I will explain the document step by step.")
        if intent == "QUIZ":
            return AgentReply(intent=intent, action="QUIZ", response="Starting quiz mode now.")
        if intent == "FLASHCARDS":
            return AgentReply(intent=intent, action="FLASHCARDS", response="Opening flashcards for quick revision.")
        if intent == "PAUSE":
            return AgentReply(intent=intent, action="PAUSE", response="Paused. Task completed. What else can I do for you?")

        return AgentReply(
            intent="CHAT",
            action="CHAT",
            response="Task completed. What else can I do for you?",
        )
