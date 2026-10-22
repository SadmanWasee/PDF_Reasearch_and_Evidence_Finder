
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from backend.app.pdf_processor import extract_pdf_text

app = FastAPI(
    title="PDF Research and Evidence Finder",
    description="Search research PDFs and retrieve relevant evidence.",
    version="1.0.0",
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class PageText(BaseModel):
    page_number: int
    text: str


class PDFUploadResponse(BaseModel):
    filename: str
    page_count: int
    pages: list[PageText]


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
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file.",
        )

    pdf_bytes = await file.read(MAX_FILE_SIZE + 1)

    if len(pdf_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="The PDF exceeds the 10 MB upload limit.",
        )

    try:
        pages = extract_pdf_text(pdf_bytes)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a readable PDF.",
        ) from exc

    if not pages:
        raise HTTPException(
            status_code=422,
            detail="No extractable text found. The PDF may be scanned.",
        )

    return {
        "filename": file.filename,
        "page_count": len(pages),
        "pages": pages,
    }
