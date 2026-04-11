from __future__ import annotations

import asyncio

from services.voice_pipeline import VoicePipeline, VoicePipelineError


class VoiceAgentError(Exception):
    pass


class VoiceAgent:
    def __init__(self, voice_pipeline: VoicePipeline) -> None:
        self.voice_pipeline = voice_pipeline

    def format_tutor_speech(self, text: str) -> str:
        clean = " ".join((text or "").split())
        if not clean:
            return ""
        clean = clean.replace(". ", "... ")
        clean = clean.replace("? ", "?... ")
        return clean

    async def synthesize(self, text: str) -> bytes:
        script = self.format_tutor_speech(text)
        if not script:
            raise VoiceAgentError("Speech text is empty.")
        try:
            return await asyncio.to_thread(self.voice_pipeline.synthesize_tutor_audio, script)
        except VoicePipelineError as ex:
            raise VoiceAgentError(str(ex)) from ex
