from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

import librosa
import soundfile as sf
from huggingface_hub import snapshot_download


class RVCServiceError(Exception):
    pass


class RVCService:
    def __init__(self) -> None:
        self.repo_id = os.getenv("RVC_MODEL_REPO", "")
        self.model_filename = os.getenv("RVC_MODEL_FILENAME", "model.pth")
        self.index_filename = os.getenv("RVC_INDEX_FILENAME", "model.index")
        self.infer_script = os.getenv("RVC_INFER_SCRIPT", "")
        self.model_dir: Path | None = None

    def convert_voice(self, audio_path: str) -> bytes:
        src = Path(audio_path)
        if not src.exists():
            raise RVCServiceError("Input TTS audio file not found.")

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            output_path = Path(tmp.name)

        try:
            converted = self._try_rvc_script(src, output_path)
            if not converted:
                self._fallback_voice_color(src, output_path)

            data = output_path.read_bytes()
            if not data:
                raise RVCServiceError("Voice conversion generated empty audio.")
            return data
        except Exception as ex:
            raise RVCServiceError(f"RVC conversion failed: {ex}") from ex
        finally:
            output_path.unlink(missing_ok=True)

    def _try_rvc_script(self, input_path: Path, output_path: Path) -> bool:
        if not self.infer_script:
            return False
        script = Path(self.infer_script)
        if not script.exists():
            return False

        self._ensure_model_downloaded()

        model_path = self._resolve_model_file(self.model_filename)
        index_path = self._resolve_model_file(self.index_filename)
        if model_path is None:
            return False

        command = [
            "python",
            str(script),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--model",
            str(model_path),
        ]
        if index_path is not None:
            command.extend(["--index", str(index_path)])

        result = subprocess.run(command, capture_output=True, text=True)
        return result.returncode == 0 and output_path.exists() and output_path.stat().st_size > 0

    def _ensure_model_downloaded(self) -> None:
        if self.model_dir is not None or not self.repo_id:
            return
        try:
            path = snapshot_download(repo_id=self.repo_id, allow_patterns=["*.pth", "*.index", "*.pt", "*.onnx"])
            self.model_dir = Path(path)
        except Exception:
            self.model_dir = None

    def _resolve_model_file(self, filename: str) -> Path | None:
        if not self.model_dir:
            return None
        direct = self.model_dir / filename
        if direct.exists():
            return direct
        matches = list(self.model_dir.rglob(filename))
        return matches[0] if matches else None

    def _fallback_voice_color(self, input_path: Path, output_path: Path) -> None:
        samples, sr = librosa.load(str(input_path), sr=None, mono=True)
        shifted = librosa.effects.pitch_shift(samples, sr=sr, n_steps=2.0)
        sf.write(str(output_path), shifted, sr)
