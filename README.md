# Project Demo: 
<div align="center">

<a href="https://www.youtube.com/watch?v=EmBaggxFL_k">
  <img src="https://img.youtube.com/vi/EmBaggxFL_k/maxresdefault.jpg" alt="Evidence Desk Project Demo" width="800">
</a>

**▶ Watch the Evidence Desk Demo**

</div>

---

# Evidence Desk — PDF Research and Evidence Finder

Evidence Desk is a web application for finding useful passages in PDF research papers and technical documents. It combines traditional keyword search with semantic search, allowing users to look for information by exact terms or by meaning.

## Live Demo

- **Application:** https://pdfreasearchfinder.vercel.app/
- **Video walkthrough:** https://www.youtube.com/watch?v=EmBaggxFL_k
- **Backend API:** https://pdf-reasearch-and-evidence-finder-1.onrender.com

## Why I Built It

Finding a specific claim or explanation inside a long PDF can mean scrolling through pages or trying several keyword searches. Those searches can miss useful passages when the document uses different wording.

Evidence Desk explores a more flexible approach: it lets users compare keyword-based retrieval, meaning-based retrieval, and a combination of both in one interface.

## Features

- Upload PDF documents for text extraction and processing.
- Split extracted text into smaller chunks for more focused retrieval.
- Search using **BM25 keyword search**.
- Search using **semantic similarity** with a pretrained text-embedding model.
- Use **hybrid search** to combine keyword and semantic rankings.
- View matching passages with document page information and relevance scores where available.
- Use a React-based interface backed by a FastAPI service.

## How It Works

The document processing and search workflow follows these steps:

1. **Upload:** The user uploads a PDF.
2. **Extract and chunk:** The backend extracts the text and divides it into smaller passages.
3. **Create embeddings:** A pretrained embedding model converts passages into vector representations.
4. **Retrieve results:** The selected search method ranks passages against the user's query.
5. **Display evidence:** The frontend presents relevant passages for review.

### Search Methods

| Method | How it works | Best suited for |
|---|---|---|
| **BM25** | Ranks passages using term frequency and document-level statistics. | Queries with specific keywords or terminology. |
| **Semantic search** | Compares query and passage embeddings to identify similar meanings. | Queries where relevant text may use different wording. |
| **Hybrid search** | Combines keyword and semantic rankings using Reciprocal Rank Fusion (RRF). | Queries where both exact terms and broader meaning matter. |

Hybrid search uses Reciprocal Rank Fusion to combine the two ranked lists without requiring their raw scores to be directly comparable.

## Technology Stack

- **Frontend:** React, Vite, Tailwind CSS
- **Backend:** Python, FastAPI
- **Text embeddings:** FastEmbed with `sentence-transformers/all-MiniLM-L6-v2`
- **Retrieval:** BM25, semantic similarity, Reciprocal Rank Fusion (RRF)
- **Data processing:** PDF text extraction, text chunking, NumPy
- **Deployment:** Vercel (frontend), Render (backend)
- **Version control:** Git and GitHub

## Try the Live App

1. Open the [Evidence Desk application](https://pdfreasearchfinder.vercel.app/).
2. Choose a PDF and upload it.
3. Allow the document to finish processing. Text extraction, chunking, and embedding generation may take a few minutes, depending on the document and available server resources.
4. Enter a question or search phrase.
5. Compare results from BM25, semantic, and hybrid search.

For a visual walkthrough, watch the [project demo on YouTube](https://www.youtube.com/watch?v=EmBaggxFL_k).

## Run Locally

### Prerequisites

- Python 3.12
- Node.js and npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/SadmanWasee/PDF_Reasearch_and_Evidence_Finder.git
cd PDF_Reasearch_and_Evidence_Finder
```

### 2. Start the Backend

Create and activate a virtual environment from the project root:

```bash
py -3.12 -m venv .venv
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the backend dependencies using the dependency file included in the project. If the backend has a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Start FastAPI from the directory containing `main.py`:

```bash
uvicorn main:app --reload
```

The API should be available at `http://127.0.0.1:8000`. Interactive API documentation is usually available at `http://127.0.0.1:8000/docs`.

> **Note:** Run the command from the directory containing `main.py`. The exact dependency-file location depends on the repository structure.

### 3. Start the Frontend

Open a second terminal and move to the frontend directory:

```bash
cd frontend
npm install
npm run dev
```

Vite will print the local development URL, usually `http://localhost:5173`.

> **API configuration:** Make sure the frontend is configured to use your local FastAPI URL during development. If the project uses an environment variable for the API base URL, check the frontend configuration and use the variable name defined in the code.

## Project Structure

The application separates the frontend interface from the backend processing and search logic.

```text
PDF_Reasearch_and_Evidence_Finder/
├── frontend/       # React, Vite, and Tailwind CSS interface
└── backend/        # FastAPI endpoints and document-search logic
```

The actual backend folder name may differ depending on the current repository layout.

## Limitations

- **Processing time:** Uploading and preparing a PDF can take a few minutes, especially on a free hosting instance.
- **In-memory storage:** Uploaded document data is held in memory rather than a persistent database. Documents may be lost when the backend process restarts or the hosting service recycles the instance.
- **PDF text quality:** Search quality depends on whether text can be extracted from the PDF. Scanned documents containing images rather than selectable text may require OCR, which is not currently part of the documented workflow.
- **Retrieval is not verification:** The app retrieves passages that may be relevant to a query. Users should read the surrounding context and consult the original document before treating a passage as evidence.

## Future Improvements

Potential improvements include persistent document storage, better handling of scanned PDFs, retrieval-quality evaluation on a labelled test set, and more detailed document-management features.

## Author

**Sadman Wasee**

Evidence Desk was developed as an AI engineering capstone to explore how NLP and information-retrieval techniques can be combined in a practical web application.
