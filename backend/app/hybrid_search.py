from backend.app.retrieval import bm25_search
from backend.app.semantic_search import semantic_search


def hybrid_search(
    chunks: list[dict],
    query: str,
    top_k: int = 5,
    rrf_k: int = 60,
) -> list[dict]:
    """Combine BM25 and semantic rankings using RRF."""

    if not query.strip() or not chunks or top_k <= 0:
        return []

    # Get rankings from both retrieval methods
    bm25_results = bm25_search(
        chunks, query, top_k=len(chunks)
    )
    semantic_results = semantic_search(
        chunks, query, top_k=len(chunks)
    )

    # Store each chunk and its combined RRF score
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

    # Return chunks with the highest combined scores
    results = sorted(
        fused.values(),
        key=lambda item: item["rrf_score"],
        reverse=True,
    )[:top_k]

    for result in results:
        result["rrf_score"] = round(result["rrf_score"], 6)

    return results
