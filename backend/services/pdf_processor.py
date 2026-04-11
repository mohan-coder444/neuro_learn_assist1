from __future__ import annotations

import io
import logging
import os
import re

import pdfplumber
import pytesseract
from PIL import Image

from models.document_model import DocumentChunk

logger = logging.getLogger(__name__)

tesseract_cmd = os.getenv("TESSERACT_CMD", "").strip()
if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd


class PDFProcessingError(Exception):
    pass


def _normalize_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _is_text_too_short(text: str, minimum_chars: int = 200) -> bool:
    return len(text.strip()) < minimum_chars


def _extract_with_pdfplumber(file_bytes: bytes) -> list[tuple[int, str]]:
    pages: list[tuple[int, str]] = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for index, page in enumerate(pdf.pages, start=1):
            extracted = page.extract_text() or ""
            pages.append((index, _normalize_text(extracted)))
    return pages


def _extract_with_ocr(file_bytes: bytes) -> list[tuple[int, str]]:
    pages: list[tuple[int, str]] = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for index, page in enumerate(pdf.pages, start=1):
            try:
                page_image = page.to_image(resolution=300)
                pil_image: Image.Image = page_image.original.convert("RGB")
                text = pytesseract.image_to_string(pil_image)
                pages.append((index, _normalize_text(text)))
            except Exception as ex:
                logger.warning("OCR failed on page %s: %s", index, ex)
                pages.append((index, ""))
    return pages


def extract_text_from_pdf(file: bytes) -> str:
    """
    Extract text from PDF by trying native extraction first, then OCR fallback.
    """
    if not file:
        raise PDFProcessingError("Empty PDF file uploaded.")

    try:
        native_pages = _extract_with_pdfplumber(file)
    except Exception as ex:
        raise PDFProcessingError(f"Could not parse PDF: {ex}") from ex

    native_text = "\n\n".join(text for _, text in native_pages if text)
    # Ultra-fast path: if native extraction has any text, skip OCR entirely.
    if native_text.strip():
        return native_text

    logger.info("Native extraction too short; trying OCR fallback.")
    ocr_pages = _extract_with_ocr(file)
    ocr_text = "\n\n".join(text for _, text in ocr_pages if text)

    final_text = ocr_text if len(ocr_text) > len(native_text) else native_text
    if _is_text_too_short(final_text, minimum_chars=50):
        raise PDFProcessingError("Failed to extract usable text from PDF.")
    return final_text


def chunk_document(document_text: str, chunk_size_tokens: int = 500, overlap_tokens: int = 50) -> list[DocumentChunk]:
    """
    Token-aware chunking approximation using words as token proxies.
    Metadata includes page_number, section and content.
    """
    if not document_text or not document_text.strip():
        raise PDFProcessingError("Document text is empty.")

    words = document_text.split()
    if not words:
        raise PDFProcessingError("Document text has no valid tokens.")

    chunks: list[DocumentChunk] = []
    step = max(1, chunk_size_tokens - overlap_tokens)

    for i in range(0, len(words), step):
        block = words[i : i + chunk_size_tokens]
        if not block:
            continue
        content = " ".join(block).strip()
        if not content:
            continue

        chunk_index = len(chunks) + 1
        section = _guess_section(content)
        chunk = DocumentChunk(
            chunk_id=f"chunk_{chunk_index}",
            page_number=_estimate_page_from_position(i),
            section=section,
            content=content,
        )
        chunks.append(chunk)

    return chunks


def _guess_section(content: str) -> str:
    # Lightweight section heuristic.
    first_sentence = re.split(r"[.!?]", content, maxsplit=1)[0].strip()
    words = first_sentence.split()
    return " ".join(words[:8]) if words else "General"


def _estimate_page_from_position(word_index: int, words_per_page: int = 350) -> int:
    return max(1, (word_index // words_per_page) + 1)
