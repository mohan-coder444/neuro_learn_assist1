from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EmotionResult:
    tone: str
    is_confused: bool
    encouragement: str


_CONFUSION_PHRASES = [
    "i don't understand",
    "this is confusing",
    "i don't know",
    "not sure",
    "i am confused",
    "hard to follow",
]


class EmotionDetector:
    def detect(self, student_text: str) -> EmotionResult:
        text = (student_text or "").strip().lower()
        confused = any(phrase in text for phrase in _CONFUSION_PHRASES)

        if confused:
            return EmotionResult(
                tone="supportive",
                is_confused=True,
                encouragement="No worries. Let's go through it step by step.",
            )

        return EmotionResult(
            tone="neutral",
            is_confused=False,
            encouragement="Great effort. Let's keep going.",
        )
