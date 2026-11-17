import re


def split_text(text: str, chunk_size: int = 1200, overlap: int = 150) -> list[str]:
    if not text or not text.strip():
        return []

    cleaned = re.sub(r"\r\n?", "\n", text).strip()
    if not cleaned:
        return []

    paragraphs = [part.strip() for part in re.split(r"\n\s*\n+", cleaned) if part.strip()]
    if not paragraphs:
        return [cleaned]

    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        if not current:
            current = paragraph
            continue

        if len(current) + 1 + len(paragraph) <= chunk_size:
            current = f"{current}\n\n{paragraph}"
            continue

        chunks.append(current)
        if overlap > 0:
            overlap_text = current[-overlap:]
            current = f"{overlap_text}\n\n{paragraph}"
        else:
            current = paragraph

    if current:
        chunks.append(current)

    final_chunks = []
    for chunk in chunks:
        if len(chunk) <= chunk_size:
            final_chunks.append(chunk)
            continue

        words = re.split(r"\s+", chunk.strip())
        buffer = ""
        for word in words:
            candidate = f"{buffer} {word}".strip()
            if len(candidate) <= chunk_size:
                buffer = candidate
                continue

            if buffer:
                final_chunks.append(buffer)
            buffer = word

        if buffer:
            final_chunks.append(buffer)

    return final_chunks or [cleaned]
