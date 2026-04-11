from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AccessibilityMode(str, Enum):
    VISUAL = "visual"
    AUDIO = "audio"
    BRAILLE = "braille"
    COMBINED = "combined"


class DocumentChunk(BaseModel):
    chunk_id: str
    page_number: int = 0
    section: str = "General"
    content: str


class StoredDocument(BaseModel):
    filename: str
    text: str
    chunks: list[DocumentChunk] = Field(default_factory=list)


class FlashcardItem(BaseModel):
    question: str
    answer: str


class QuizItem(BaseModel):
    question: str
    options: list[str]
    correct_answer: str
    explanation: str


class ChatRequest(BaseModel):
    question: str


class VoiceRequest(BaseModel):
    text: str
    voice_id: str | None = None
    speed: float = 1.0


class BrailleRequest(BaseModel):
    text: str
    port: str | None = None
    baud_rate: int = 9600


class AccessibilitySettings(BaseModel):
    mode: AccessibilityMode = AccessibilityMode.VISUAL
    voice_speed: float = 1.0
    auto_read_aloud: bool = False
    braille_enabled: bool = False
    high_contrast: bool = False


class ApiMessage(BaseModel):
    status: str
    detail: str
    data: dict[str, Any] | None = None
