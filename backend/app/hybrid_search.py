
from backend.app.retrieval import bm25_search
from backend.app.semantic_search import semantic_search
import numpy as np


def hybrid_search(
    chunks: list[dict],
    query: str,
    top_k: int = 5,
    rrf_k: int = 60,
    chunk_embeddings: np.ndarray | None = None,
) -> list[dict]:
    """Combine BM25 and semantic rankings using Reciprocal Rank Fusion."""

    if not query.strip() or not chunks or top_k <= 0:
        return []

    # Retrieve keyword-based results.
    bm25_results = bm25_search(
        chunks,
        query,
        top_k=len(chunks),
    )

    # Retrieve semantic results using cached embeddings when available.
    semantic_results = semantic_search(
        chunks,
        query,
        top_k=len(chunks),
        chunk_embeddings=chunk_embeddings,
    )

    # Combine the rankings using Reciprocal Rank Fusion (RRF).
    fused = {}

    for ranking in (bm25_results, semantic_results):
        for rank, result in enumerate(ranking, start=1):
            key = (result["page_number"], result["chunk_id"])

            if key not in fused:
                fused[key] = {
                    **result,
                    "rrf_score": 0.0,
                }

            fused[key]["rrf_score"] += 1 / (rrf_k + rank)

    results = sorted(
        fused.values(),
        key=lambda item: item["rrf_score"],
        reverse=True,
    )[:top_k]

    for result in results:
        result["rrf_score"] = round(
            result["rrf_score"],
            6,
        )

    return results
