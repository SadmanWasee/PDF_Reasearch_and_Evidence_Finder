
import re

from rank_bm25 import BM25Okapi


def tokenize(text: str) -> list[str]:
    """Convert text into lowercase word tokens."""
    return re.findall(r"\b\w+\b", text.lower())


def bm25_search(
    chunks: list[dict],
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """Return the most relevant text chunks using BM25."""

    if not query.strip() or not chunks or top_k <= 0:
        return []

    # Tokenize each chunk to prepare the searchable corpus
    tokenized_chunks = [
        tokenize(chunk["text"])
        for chunk in chunks
    ]

    # Build the BM25 ranking model
    bm25 = BM25Okapi(tokenized_chunks)

    # Calculate relevance scores for the query
    query_tokens = tokenize(query)
    scores = bm25.get_scores(query_tokens)

    # Rank chunks from highest to lowest score
    ranked_indices = sorted(
        range(len(chunks)),
        key=lambda index: scores[index],
        reverse=True,
    )

    # Return the top results with their source information
    results = []

    for index in ranked_indices[:top_k]:
        if scores[index] <= 0:
            continue

        result = {
            **chunks[index],
            "score": round(float(scores[index]), 4),
        }
        results.append(result)

    return results
