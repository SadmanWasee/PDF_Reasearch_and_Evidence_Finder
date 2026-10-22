
from fastapi import FastAPI

app = FastAPI(
    title="PDF Research and Evidence Finder",
    description="Search research PDFs and retrieve relevant evidence.",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "PDF Research and Evidence Finder API is running!"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
