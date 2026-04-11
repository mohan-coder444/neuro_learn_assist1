from __future__ import annotations

import os

import requests


class VoiceServiceError(Exception):
    pass


class VoiceService:
    def __init__(self) -> None:
        self.api_key = os.getenv("ELEVENLABS_API_KEY", "")
        self.default_voice_id = os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")

    def generate_speech(self, text: str, voice_id: str | None = None, speed: float = 1.0) -> bytes:
        if not text.strip():
            raise VoiceServiceError("Text for speech is empty.")
        if not self.api_key:
            raise VoiceServiceError("ELEVENLABS_API_KEY is not configured.")

        selected_voice = voice_id or self.default_voice_id
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{selected_voice}"

        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.45,
                "similarity_boost": 0.8,
                "style": 0.2,
                "use_speaker_boost": True,
                "speed": max(0.7, min(speed, 1.2)),
            },
        }

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key,
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            if response.status_code >= 400:
                raise VoiceServiceError(f"ElevenLabs API error: {response.status_code} {response.text}")
            return response.content
        except requests.RequestException as ex:
            raise VoiceServiceError(f"Voice generation failed: {ex}") from ex
