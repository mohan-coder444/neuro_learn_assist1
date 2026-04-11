from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path

from services.gemini_service import GeminiService, GeminiServiceError
from services.rvc_service import RVCService, RVCServiceError
from services.stt_service import STTService, STTServiceError
from services.tts_service import TTSService, TTSServiceError


class VoicePipelineError(Exception):
    pass


class VoicePipeline:
    def __init__(self, stt: STTService, gemini: GeminiService, tts: TTSService, rvc: RVCService) -> None:
        self.stt = stt
        self.gemini = gemini
        self.tts = tts
        self.rvc = rvc

    def run(self, audio_file: bytes) -> dict[str, str | bytes]:
        try:
            transcript = self.stt.transcribe_audio(audio_file)
            answer = self.gemini.tutor_chat(transcript).strip()
            if not answer:
                raise VoicePipelineError("Gemini tutor returned an empty response.")

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tts_path = Path(tmp.name)

            self.tts.generate_speech_to_file(answer, str(tts_path))
            converted_audio = self.rvc.convert_voice(str(tts_path))

            return {
                "transcript": transcript,
                "answer": answer,
                "audio": converted_audio,
            }
        except (STTServiceError, TTSServiceError, RVCServiceError, GeminiServiceError) as ex:
            raise VoicePipelineError(str(ex)) from ex
        except Exception as ex:
            raise VoicePipelineError(f"Voice pipeline failed: {ex}") from ex
        finally:
            try:
                if 'tts_path' in locals() and tts_path.exists():
                    tts_path.unlink(missing_ok=True)
            except Exception:
                pass

    async def explain_document(self, summary_text: str) -> dict[str, str | bytes]:
        if not summary_text.strip():
            raise VoicePipelineError("Summary text is empty.")

        prompt = (
            "You are a friendly AI tutor explaining a document to a student. "
            "Explain the document step-by-step in simple language. "
            "Ask occasional questions to keep the student engaged.\n\n"
            f"SUMMARY:\n{summary_text}"
        )

        try:
            explanation = await asyncio.to_thread(self.gemini.tutor_chat, prompt)
            explanation = explanation.strip()
            if not explanation:
                raise VoicePipelineError("Gemini returned empty explanation.")

            audio_bytes = await asyncio.to_thread(self.synthesize_tutor_audio, explanation)
            return {
                "explanation": explanation,
                "audio": audio_bytes,
            }
        except (GeminiServiceError, TTSServiceError, RVCServiceError) as ex:
            raise VoicePipelineError(str(ex)) from ex
        except Exception as ex:
            raise VoicePipelineError(f"Document explanation pipeline failed: {ex}") from ex

    def synthesize_tutor_audio(self, text: str) -> bytes:
        if not text.strip():
            raise VoicePipelineError("Tutor response text is empty.")

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tts_path = Path(tmp.name)

        try:
            self.tts.generate_speech_to_file(text, str(tts_path))
            return self.rvc.convert_voice(str(tts_path))
        except (TTSServiceError, RVCServiceError) as ex:
            raise VoicePipelineError(str(ex)) from ex
        finally:
            try:
                if tts_path.exists():
                    tts_path.unlink(missing_ok=True)
            except Exception:
                pass
