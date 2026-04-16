from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from moviepy.editor import AudioFileClip, ColorClip, TextClip, CompositeVideoClip

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import AudioFileClip, VideoClip

class VideoServiceError(Exception):
    pass

class VideoService:
    def __init__(self) -> None:
        self.output_dir = Path("data/videos")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.width = 1280
        self.height = 720

    def _create_frame(self, t: float, text: str, duration: float) -> np.ndarray:
        # Create a dark navy background
        img = Image.new('RGB', (self.width, self.height), color=(5, 8, 22))
        draw = ImageDraw.Draw(img)
        
        # Load a font (fallback to default if necessary)
        try:
            # Try to find a standard Windows font
            font = ImageFont.truetype("arial.ttf", 40)
            title_font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
            title_font = ImageFont.load_default()

        # Draw Title
        draw.text((60, 60), "NeuroLearn Assist Explanation", font=title_font, fill=(59, 130, 246))

        # Draw wrapped text
        import textwrap
        clean_text = text.replace('#', '').replace('*', '').strip()
        lines = textwrap.wrap(clean_text, width=50)
        display_text = "\n".join(lines[:10]) + ("..." if len(lines) > 10 else "")
        
        draw.text((60, 160), display_text, font=font, fill=(241, 245, 249), spacing=20)
        
        # Draw Progress bar at bottom
        progress_w = int((t / duration) * self.width)
        draw.rectangle([0, self.height-10, progress_w, self.height], fill=(59, 130, 246))

        return np.array(img)

    def generate_explanation_mp4(self, text: str, audio_bytes: bytes) -> str:
        """
        Creates an MP4 file with the given text displayed over a background and the audio.
        """
        import tempfile
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as audio_tmp:
            audio_tmp.write(audio_bytes)
            audio_path = audio_tmp.name
            
        output_filename = f"explanation_{os.urandom(4).hex()}.mp4"
        output_path = str(self.output_dir / output_filename)

        try:
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration

            # Create video clip from frames
            video_clip = VideoClip(lambda t: self._create_frame(t, text, duration), duration=duration)
            video_clip = video_clip.set_audio(audio_clip)

            # Write file
            video_clip.write_videofile(
                output_path, 
                fps=10, 
                codec='libx264', 
                audio_codec='aac', 
                bitrate="1000k",
                logger=None
            )

            return output_path

        except Exception as ex:
            raise VideoServiceError(f"Video generation failed: {ex}") from ex
        finally:
            if os.path.exists(audio_path):
                os.unlink(audio_path)
