from __future__ import annotations

import os
import tempfile
from pathlib import Path

from elevenlabs.client import ElevenLabs
import librosa
import soundfile as sf


class TTSServiceError(Exception):
    pass


class TTSService:
    def __init__(self) -> None:
        self.api_key = os.getenv("ELEVENLABS_API_KEY", "").strip()
        self.client: ElevenLabs | None = ElevenLabs(api_key=self.api_key) if self.api_key else None
        self.voice = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
        self.model_id = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")

    def generate_speech(self, text: str) -> bytes:
        if not text.strip():
            raise TTSServiceError("TTS input text is empty.")
        if not self.client:
            raise TTSServiceError("ELEVENLABS_API_KEY is not configured.")

        try:
            stream = self.client.text_to_speech.convert(
                voice_id=self.voice,
                model_id=self.model_id,
                output_format="mp3_44100_128",
                text=text,
            )
            mp3_bytes = b"".join(chunk for chunk in stream if chunk)
            if not mp3_bytes:
                raise TTSServiceError("TTS returned empty audio.")

            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as mp3_tmp:
                mp3_tmp.write(mp3_bytes)
                mp3_path = Path(mp3_tmp.name)

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as wav_tmp:
                wav_path = Path(wav_tmp.name)

            samples, sr = librosa.load(str(mp3_path), sr=None, mono=True)
            sf.write(str(wav_path), samples, sr if sr else 44100)
            wav_bytes = wav_path.read_bytes()
            if not wav_bytes:
                raise TTSServiceError("TTS WAV conversion returned empty audio.")
            return wav_bytes
        except Exception as ex:
            raise TTSServiceError(f"TTS generation failed: {ex}") from ex
        finally:
            try:
                if 'mp3_path' in locals() and mp3_path.exists():
                    mp3_path.unlink(missing_ok=True)
                if 'wav_path' in locals() and wav_path.exists():
                    wav_path.unlink(missing_ok=True)
            except Exception:
                pass

    def generate_speech_to_file(self, text: str, output_path: str) -> str:
        if not text.strip():
            raise TTSServiceError("TTS input text is empty.")

        try:
            audio = self.generate_speech(text)
            Path(output_path).write_bytes(audio)
            return output_path
        except Exception as ex:
            raise TTSServiceError(f"TTS generation failed: {ex}") from ex
