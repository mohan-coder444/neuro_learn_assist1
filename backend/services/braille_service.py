from __future__ import annotations

from dataclasses import dataclass

import serial


class BrailleServiceError(Exception):
    pass


BRAILLE_MAP = {
    "a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙", "e": "⠑", "f": "⠋", "g": "⠛", "h": "⠓", "i": "⠊", "j": "⠚",
    "k": "⠅", "l": "⠇", "m": "⠍", "n": "⠝", "o": "⠕", "p": "⠏", "q": "⠟", "r": "⠗", "s": "⠎", "t": "⠞",
    "u": "⠥", "v": "⠧", "w": "⠺", "x": "⠭", "y": "⠽", "z": "⠵",
    " ": " ", ".": "⠲", ",": "⠂", "?": "⠦", "!": "⠖", "-": "⠤", ":": "⠒", ";": "⠆",
}


@dataclass
class BrailleResult:
    braille_text: str
    bytes_sent: int


class BrailleService:
    def text_to_braille(self, text: str) -> str:
        if not text:
            raise BrailleServiceError("Input text is empty.")
        return "".join(BRAILLE_MAP.get(ch.lower(), "⍰") for ch in text)

    def send_to_arduino(self, text: str, port: str = "COM3", baud_rate: int = 9600) -> BrailleResult:
        braille_text = self.text_to_braille(text)
        payload = f"{braille_text}\n".encode("utf-8")

        try:
            with serial.Serial(port=port, baudrate=baud_rate, timeout=2) as connection:
                sent = connection.write(payload)
                connection.flush()
            return BrailleResult(braille_text=braille_text, bytes_sent=sent)
        except serial.SerialException as ex:
            raise BrailleServiceError(f"Braille hardware disconnected or unavailable: {ex}") from ex
