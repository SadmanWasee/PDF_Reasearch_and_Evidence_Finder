import re


def split_into_sentences(text: str) -> list[str]:
    """Split text into sentences using common sentence-ending punctuation."""

    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", text)

    return [sentence.strip() for sentence in sentences if sentence.strip()]


def split_long_sentence(sentence: str, chunk_size: int) -> list[str]:
    """Split a sentence that exceeds the chunk size into smaller word groups."""

    words = sentence.split()
    parts = []
    current_words = []
    current_length = 0

    for word in words:
        additional_length = len(word) + (1 if current_words else 0)

        if current_words and current_length + additional_length > chunk_size:
            parts.append(" ".join(current_words))
            current_words = [word]
            current_length = len(word)
        else:
            current_words.append(word)
            current_length += additional_length

    if current_words:
        parts.append(" ".join(current_words))

    return parts


def chunk_pages(
    pages: list[dict],
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[dict]:
    """Split page text into sentence-aware chunks with overlapping context."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size.")

    chunks = []

    for page in pages:
        text = page["text"]
        page_number = page["page_number"]

        sentences = split_into_sentences(text)

        # Keep individual sentences within the target chunk size.
        segments = []

        for sentence in sentences:
            if len(sentence) > chunk_size:
                segments.extend(
                    split_long_sentence(sentence, chunk_size)
                )
            else:
                segments.append(sentence)

        current_parts = []
        current_length = 0

        for segment in segments:
            additional_length = len(segment) + (
                1 if current_parts else 0
            )

            if (
                current_parts
                and current_length + additional_length > chunk_size
            ):
                chunk_text = " ".join(current_parts).strip()

                if chunk_text:
                    chunks.append({
                        "page_number": page_number,
                        "chunk_id": len(chunks) + 1,
                        "text": chunk_text,
                    })

                # Retain recent context for the next chunk.
                overlap_parts = []
                overlap_length = 0

                for part in reversed(current_parts):
                    part_length = len(part) + (
                        1 if overlap_parts else 0
                    )

                    if overlap_length + part_length > overlap:
                        break

                    overlap_parts.insert(0, part)
                    overlap_length += part_length

                current_parts = overlap_parts
                current_length = len(" ".join(current_parts))

                # If the overlap leaves insufficient room for the next
                # segment, start a new chunk without that overlap.
                if (
                    current_parts
                    and current_length + 1 + len(segment) > chunk_size
                ):
                    current_parts = []
                    current_length = 0

            if current_parts:
                current_length += 1 + len(segment)
            else:
                current_length = len(segment)

            current_parts.append(segment)

        if current_parts:
            chunk_text = " ".join(current_parts).strip()

            if chunk_text:
                chunks.append({
                    "page_number": page_number,
                    "chunk_id": len(chunks) + 1,
                    "text": chunk_text,
                })

    return chunks