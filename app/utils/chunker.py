from typing import List
import re


def chunk_text(text: str, max_chars: int = 800, overlap: int = 100) -> List[str]:
    normalized_text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized_text:
        return []

    paragraphs = _split_paragraphs(normalized_text)

    chunks: List[str] = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + (1 if current_chunk else 0) <= max_chars:
            current_chunk = f"{current_chunk}\n{paragraph}".strip(
            ) if current_chunk else paragraph
            continue

        if current_chunk:
            chunks.append(current_chunk)
            current_chunk = ""

        if len(paragraph) <= max_chars:
            chunks.append(paragraph)
            continue

        step = max_chars - overlap
        for start in range(0, len(paragraph), step):
            window = paragraph[start:start + max_chars]
            chunks.append(window)

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


_PARAGRAPH_SPLIT_PATTERN = re.compile(r"\n\s*\n|\n#|\n-{3,}|\n={3,}")


def _split_paragraphs(text: str) -> List[str]:
    raw_parts = _PARAGRAPH_SPLIT_PATTERN.split(text)
    return [part.strip() for part in raw_parts if part and part.strip()]
