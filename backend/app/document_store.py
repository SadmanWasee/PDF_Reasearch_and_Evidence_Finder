from uuid import uuid4

import numpy as np


# Stores uploaded documents until the server restarts.
documents: dict[str, dict] = {}


def save_document(
    filename: str,
    pages: list[dict],
    chunks: list[dict],
    embeddings: np.ndarray | None = None,
) -> str:
    """Store a document, its chunks, and its embeddings."""

    document_id = str(uuid4())

    documents[document_id] = {
        "filename": filename,
        "pages": pages,
        "chunks": chunks,
        "embeddings": embeddings,
    }

    return document_id


def get_document(document_id: str) -> dict | None:
    """Retrieve a stored document by its ID."""

    return documents.get(document_id)
