import numpy as np
from fastembed import TextEmbedding

# Load the embedding model once when the application starts.
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = TextEmbedding(model_name=MODEL_NAME)


def generate_embeddings(chunks: list[dict]) -> np.ndarray:
    """Generate and return embeddings for document chunks."""

    texts = [chunk["text"] for chunk in chunks]

    # Process texts in small batches to limit temporary memory usage.
    embeddings = model.embed(texts, batch_size=8)

    # Convert the embeddings into a single float32 array.
    return np.asarray(list(embeddings), dtype=np.float32)


def semantic_search(
    chunks: list[dict],
    query: str,
    top_k: int = 5,
    chunk_embeddings: np.ndarray | None = None,
) -> list[dict]:
    """Find the document chunks most semantically similar to a query."""

    if not query.strip() or not chunks or top_k <= 0:
        return []

    # Reuse cached embeddings when available.
    if chunk_embeddings is None:
        chunk_embeddings = generate_embeddings(chunks)

    # Embed only the user's query.
    query_embedding = next(model.query_embed(query))
    query_embedding = np.asarray(query_embedding, dtype=np.float32)

    # Calculate cosine similarity without sklearn's extra allocations.
    query_norm = np.linalg.norm(query_embedding)
    chunk_norms = np.linalg.norm(chunk_embeddings, axis=1)

    denominator = chunk_norms * query_norm
    scores = np.zeros(len(chunks), dtype=np.float32)

    valid = denominator > 0
    scores[valid] = (
        chunk_embeddings[valid] @ query_embedding
    ) / denominator[valid]

    # Select only the highest-scoring chunks.
    top_k = min(top_k, len(chunks))
    ranked_indices = np.argsort(scores)[-top_k:][::-1]

    results = []

    for index in ranked_indices:
        result = {
            **chunks[int(index)],
            "score": round(float(scores[index]), 4),
        }
        results.append(result)

    return results