from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CommandResult:
    action: str
    normalized_text: str
    requires_wake_word: bool = False


WAKE_WORDS = ["jarvis", "neurolearn", "hey tutor"]


def parse_voice_command(command_text: str) -> CommandResult:
    text = (command_text or "").strip().lower()

    if any(word in text for word in WAKE_WORDS):
        return CommandResult(action="WAKE", normalized_text=text, requires_wake_word=False)

    if any(phrase in text for phrase in ["upload pdf", "upload file", "open file", "open file manager"]):
        return CommandResult(action="UPLOAD", normalized_text=text, requires_wake_word=True)
    if any(phrase in text for phrase in ["start explanation", "explain", "start explain", "begin explanation"]):
        return CommandResult(action="EXPLAIN", normalized_text=text, requires_wake_word=True)
    if any(phrase in text for phrase in ["start quiz", "quiz", "begin quiz"]):
        return CommandResult(action="QUIZ", normalized_text=text, requires_wake_word=True)
    if any(phrase in text for phrase in ["open flashcards", "flashcards", "show flashcards"]):
        return CommandResult(action="FLASHCARDS", normalized_text=text, requires_wake_word=True)
    if any(phrase in text for phrase in ["next question", "next"]):
        return CommandResult(action="NEXT", normalized_text=text, requires_wake_word=True)
    if any(phrase in text for phrase in ["repeat explanation", "explain again", "repeat"]):
        return CommandResult(action="REPEAT", normalized_text=text, requires_wake_word=True)
    if any(phrase in text for phrase in ["pause tutor", "pause", "stop tutor", "hold on"]):
        return CommandResult(action="PAUSE", normalized_text=text, requires_wake_word=True)

    return CommandResult(action="CHAT", normalized_text=text, requires_wake_word=True)


def detect_intent(text: str) -> str:
    parsed = parse_voice_command(text)
    return parsed.action
