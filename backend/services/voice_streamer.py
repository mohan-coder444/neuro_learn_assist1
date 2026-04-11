from __future__ import annotations

import asyncio
import threading
from dataclasses import dataclass
from typing import AsyncGenerator

import google.generativeai as genai

from services.gemini_service import GeminiService, GeminiServiceError
from services.rvc_service import RVCService, RVCServiceError
from services.tts_service import TTSService, TTSServiceError


class VoiceStreamerError(Exception):
    pass


@dataclass
class StreamChunk:
    index: int
    text: str
    audio: bytes


class VoiceStreamer:
    def __init__(self, gemini: GeminiService, tts: TTSService, rvc: RVCService) -> None:
        self.gemini = gemini
        self.tts = tts
        self.rvc = rvc

    async def stream_explanation(self, context_text: str) -> AsyncGenerator[StreamChunk, None]:
        if not context_text.strip():
            raise VoiceStreamerError("No context available for streaming explanation.")

        prompt = (
            "You are NeuroLearn AI Tutor.\n\n"
            "Speak like a calm, intelligent professor explaining a concept to a student.\n"
            "Rules:\n"
            "- Explain step by step\n"
            "- Use simple language\n"
            "- Pause between ideas with short, natural phrases\n"
            "- Ask questions occasionally\n"
            "- Encourage the student\n"
            "- Speak naturally like a human tutor\n\n"
            "Structure:\n"
            "1. Start with a simple introduction\n"
            "2. Explain key ideas step by step\n"
            "3. Use examples\n"
            "4. Ask a question after explaining\n"
            "5. Encourage the student\n\n"
            f"Document:\n{context_text[:12000]}"
        )

        try:
            idx = 0
            async for chunk_text in self.stream_text(prompt):
                wav = await asyncio.to_thread(self.tts.generate_speech, chunk_text)
                converted = await asyncio.to_thread(self._convert_wav_bytes, wav)
                yield StreamChunk(index=idx, text=chunk_text, audio=converted)
                idx += 1
        except (GeminiServiceError, TTSServiceError, RVCServiceError) as ex:
            raise VoiceStreamerError(str(ex)) from ex
        except Exception as ex:
            raise VoiceStreamerError(f"Voice streaming failed: {ex}") from ex

    async def stream_text(self, prompt: str, max_chars: int = 220) -> AsyncGenerator[str, None]:
        loop = asyncio.get_running_loop()
        queue: asyncio.Queue[str | None] = asyncio.Queue()
        error_box: list[Exception] = []

        def producer() -> None:
            try:
                for piece in self._gemini_stream_iter(prompt):
                    loop.call_soon_threadsafe(queue.put_nowait, piece)
            except Exception as ex:
                error_box.append(ex)
            finally:
                loop.call_soon_threadsafe(queue.put_nowait, None)

        thread = threading.Thread(target=producer, daemon=True)
        thread.start()

        buffer = ""
        seen_piece = False
        while True:
            piece = await queue.get()
            if piece is None:
                break
            if not piece.strip():
                continue
            seen_piece = True
            buffer = f"{buffer} {piece}".strip()
            while len(buffer) >= max_chars:
                cut = self._safe_cut(buffer, max_chars)
                yield cut.strip()
                buffer = buffer[len(cut):].strip()

        if not seen_piece and error_box:
            text = await asyncio.to_thread(self.gemini.tutor_chat, prompt)
            for chunk in self._chunk_text(text.strip(), max_chars=max_chars):
                if chunk:
                    yield chunk
            return

        if buffer.strip():
            yield buffer.strip()

    async def greeting_audio(self, message: str) -> bytes:
        try:
            wav = await asyncio.to_thread(self.tts.generate_speech, message)
            return await asyncio.to_thread(self._convert_wav_bytes, wav)
        except (TTSServiceError, RVCServiceError) as ex:
            raise VoiceStreamerError(str(ex)) from ex

    def _convert_wav_bytes(self, wav_bytes: bytes) -> bytes:
        import tempfile
        from pathlib import Path

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as src_file:
            src_file.write(wav_bytes)
            src_path = Path(src_file.name)

        try:
            return self.rvc.convert_voice(str(src_path))
        finally:
            src_path.unlink(missing_ok=True)

    def _chunk_text(self, text: str, max_chars: int) -> list[str]:
        sentences = [part.strip() for part in text.replace("\n", " ").split(".") if part.strip()]
        if not sentences:
            return [text[:max_chars]]

        chunks: list[str] = []
        current = ""
        for sentence in sentences:
            sentence = f"{sentence}."
            if len(current) + len(sentence) <= max_chars:
                current = f"{current} {sentence}".strip()
            else:
                if current:
                    chunks.append(current)
                current = sentence
        if current:
            chunks.append(current)
        return chunks

    def _safe_cut(self, text: str, max_chars: int) -> str:
        if len(text) <= max_chars:
            return text
        window = text[:max_chars]
        for mark in [". ", "? ", "! ", "; ", ", ", " "]:
            pos = window.rfind(mark)
            if pos > 30:
                return window[: pos + 1]
        return window

    def _gemini_stream_iter(self, prompt: str):
        model_candidates = getattr(self.gemini, "model_candidates", ["gemini-1.5-flash"])
        last_error: Exception | None = None

        for model_name in model_candidates:
            try:
                stream = genai.GenerativeModel(model_name).generate_content(prompt, stream=True)
                emitted = False
                for part in stream:
                    text = getattr(part, "text", "") or ""
                    if text:
                        emitted = True
                        yield text
                if emitted:
                    return
            except Exception as ex:
                last_error = ex
                continue

        raise VoiceStreamerError(f"Gemini streaming unavailable: {last_error}")
