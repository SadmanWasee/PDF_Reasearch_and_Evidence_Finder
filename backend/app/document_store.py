
from uuid import uuid4


# Stores uploaded documents until the server restarts
documents: dict[str, dict] = {}


def save_document(
    filename: str,
    pages: list[dict],
    chunks: list[dict],
) -> str:
    """Store an uploaded document and return its unique ID."""

    document_id = str(uuid4())

    documents[document_id] = {
        "filename": filename,
        "pages": pages,
        "chunks": chunks,
    }

    return document_id


def get_document(document_id: str) -> dict | None:
    """Retrieve a stored document by its ID."""

    return documents.get(document_id)
