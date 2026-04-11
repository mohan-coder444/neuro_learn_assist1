from __future__ import annotations

from dataclasses import dataclass

from services.command_parser import detect_intent


@dataclass
class CommandDecision:
    action: str
    intent: str
    requires_document: bool
    requires_wake_word: bool


class CommandAgent:
    WAKE_WORDS = ("jarvis", "neurolearn", "hey tutor")

    def decide(self, user_input: str) -> CommandDecision:
        text = (user_input or "").strip().lower()
        if not text:
            return CommandDecision(action="CHAT", intent="CHAT", requires_document=False, requires_wake_word=True)

        if any(word in text for word in self.WAKE_WORDS):
            return CommandDecision(action="WAKE", intent="WAKE", requires_document=False, requires_wake_word=False)

        intent = detect_intent(text)

        action_map = {
            "UPLOAD": ("UPLOAD_DOC", False),
            "EXPLAIN": ("EXPLAIN_DOC", True),
            "QUIZ": ("START_QUIZ", True),
            "FLASHCARDS": ("OPEN_FLASHCARDS", True),
            "REPEAT": ("REPEAT_EXPLANATION", True),
            "NEXT": ("NEXT_QUESTION", True),
            "PAUSE": ("PAUSE", False),
        }

        action, needs_doc = action_map.get(intent, ("CHAT", True))
        return CommandDecision(
            action=action,
            intent=intent,
            requires_document=needs_doc,
            requires_wake_word=True,
        )
