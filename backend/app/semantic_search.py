
import numpy as np
from fastembed import TextEmbedding
from sklearn.metrics.pairwise import cosine_similarity

# Load the lightweight ONNX embedding model once.
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = TextEmbedding(model_name=MODEL_NAME)


def semantic_search(
    chunks: list[dict],
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """Find chunks that are semantically similar to a query."""

    if not query.strip() or not chunks or top_k <= 0:
        return []

    # Generate embeddings for the PDF chunks.
    texts = [chunk["text"] for chunk in chunks]
    chunk_embeddings = np.array(list(model.embed(texts)))

    # Generate an embedding for the search query.
    query_embedding = np.array(list(model.query_embed(query)))

    # Compare the query with every chunk.
    scores = cosine_similarity(
        query_embedding,
        chunk_embeddings,
    )[0]

    # Return the most similar chunks first.
    ranked_indices = scores.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indices:
        result = {
            **chunks[int(index)],
            "score": round(float(scores[index]), 4),
        }
        results.append(result)

    return results
