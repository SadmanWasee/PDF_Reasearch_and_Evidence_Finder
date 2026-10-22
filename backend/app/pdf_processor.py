
import pymupdf


def extract_pdf_text(pdf_bytes: bytes) -> list[dict]:
    """Extract text from each page of a PDF."""

    pages = []

    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            if text:
                pages.append({
                    "page_number": page_number,
                    "text": text,
                })

    return pages
