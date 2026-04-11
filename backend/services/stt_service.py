from __future__ import annotations

import tempfile
from pathlib import Path

import librosa
from transformers import pipeline


class STTServiceError(Exception):
    pass


class STTService:
    def __init__(self) -> None:
        self.model_id = "facebook/wav2vec2-base-960h"
        self._asr = None

    def _get_asr(self):
        if self._asr is None:
            self._asr = pipeline("automatic-speech-recognition", model=self.model_id)
        return self._asr

    def transcribe_audio(self, audio_file: bytes) -> str:
        if not audio_file:
            raise STTServiceError("Audio input is empty.")

        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio_file)
                audio_path = Path(tmp.name)

            samples, _ = librosa.load(str(audio_path), sr=16_000, mono=True)
            result = self._get_asr()(samples)
            text = str(result.get("text", "")).strip()
            if not text:
                raise STTServiceError("Speech recognition returned empty text.")
            return text
        except Exception as ex:
            raise STTServiceError(f"Audio transcription failed: {ex}") from ex
        finally:
            try:
                if 'audio_path' in locals() and audio_path.exists():
                    audio_path.unlink(missing_ok=True)
            except Exception:
                pass
