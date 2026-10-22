
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the model once when this module is imported
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)


def semantic_search(
    chunks: list[dict],
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """Find chunks that are semantically similar to a query."""

    if not query.strip() or not chunks or top_k <= 0:
        return []

    # Convert every chunk into a numerical embedding
    texts = [chunk["text"] for chunk in chunks]
    chunk_embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    # Convert the user's query into an embedding
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    # Compare the query embedding with every chunk embedding
    scores = cosine_similarity(
        query_embedding,
        chunk_embeddings,
    )[0]

    # Rank chunks from most to least similar
    ranked_indices = scores.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indices:
        result = {
            **chunks[int(index)],
            "score": round(float(scores[index]), 4),
        }
        results.append(result)

    return results
