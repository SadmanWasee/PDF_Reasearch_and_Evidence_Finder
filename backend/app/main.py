from backend.app.retrieval import bm25_search
from backend.app.semantic_search import semantic_search
from backend.app.hybrid_search import hybrid_search
from backend.app.schemas import SearchRequest

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from backend.app.pdf_processor import extract_pdf_text
from backend.app.chunker import chunk_pages
from backend.app.retrieval import bm25_search
from backend.app.schemas import SearchRequest

app = FastAPI(
    title="PDF Research and Evidence Finder",
    description="Search research PDFs and retrieve relevant evidence.",
    version="1.0.0",
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class PageText(BaseModel):
    page_number: int
    text: str


class TextChunk(BaseModel):
    page_number: int
    chunk_id: int
    text: str


class PDFUploadResponse(BaseModel):
    filename: str
    page_count: int
    pages: list[PageText]
    chunks: list[TextChunk]


@app.get("/")
def home():
    return {
        "message": "PDF Research and Evidence Finder API is running!"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/upload", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    # Validate the uploaded filename
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file.",
        )

    # Read the file, allowing us to detect files exceeding the limit
    pdf_bytes = await file.read(MAX_FILE_SIZE + 1)

    if len(pdf_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="The PDF exceeds the 10 MB upload limit.",
        )

    # Extract text from each PDF page
    try:
        pages = extract_pdf_text(pdf_bytes)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a readable PDF.",
        ) from exc

    # Reject PDFs without extractable text
    if not pages:
        raise HTTPException(
            status_code=422,
            detail="No extractable text found. The PDF may be scanned.",
        )

    # Split the extracted text into overlapping chunks
    chunks = chunk_pages(pages)

    # Return the extracted pages and generated chunks
    return {
        "filename": file.filename,
        "page_count": len(pages),
        "pages": pages,
        "chunks": chunks,
    }


@app.post("/search")
def search_chunks(request: SearchRequest):
    results = bm25_search(
        chunks=request.chunks,
        query=request.query,
        top_k=request.top_k,
    )

    return {
        "query": request.query,
        "result_count": len(results),
        "results": results,
    }


@app.post("/search/bm25")
def search_bm25(request: SearchRequest):
    results = bm25_search(
        chunks=request.chunks,
        query=request.query,
        top_k=request.top_k,
    )

    return {
        "method": "bm25",
        "query": request.query,
        "result_count": len(results),
        "results": results,
    }


@app.post("/search/semantic")
def search_semantic(request: SearchRequest):
    results = semantic_search(
        chunks=request.chunks,
        query=request.query,
        top_k=request.top_k,
    )

    return {
        "method": "semantic",
        "query": request.query,
        "result_count": len(results),
        "results": results,
    }


@app.post("/search/hybrid")
def search_hybrid(request: SearchRequest):
    results = hybrid_search(
        chunks=request.chunks,
        query=request.query,
        top_k=request.top_k,
    )

    return {
        "method": "hybrid",
        "query": request.query,
        "result_count": len(results),
        "results": results,
    }
