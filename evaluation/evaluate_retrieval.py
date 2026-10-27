import argparse
import csv
import sys
from pathlib import Path

# Make the project root importable when this script is run directly.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.chunker import chunk_pages
from backend.app.hybrid_search import hybrid_search
from backend.app.pdf_processor import extract_pdf_text
from backend.app.retrieval import bm25_search
from backend.app.semantic_search import semantic_search


EVALUATION_DIR = PROJECT_ROOT / "evaluation"
DEFAULT_PDF_PATH = EVALUATION_DIR / "Fact or Fiction.pdf"

QUESTIONS = [
    ("Q1", "What challenges arise when verifying scientific claims?"),
    ("Q2", "How are scientific claims obtained for the SciFact dataset?"),
    ("Q3", "What is the difference between natural and synthetic claims?"),
    ("Q4", "What role does evidence play in scientific fact-checking?"),
    ("Q5", "How are supporting and refuting evidence used in claim verification?"),
    ("Q6", "How are claims created from citation sentences?"),
    ("Q7", "Why is domain knowledge important when verifying scientific claims?"),
    ("Q8", "How does the system retrieve evidence for scientific claims?"),
    ("Q9", "What are distractor abstracts, and why are they included in the corpus?"),
    ("Q10", "How is the scientific claim verification dataset constructed?"),
]

SEARCH_METHODS = {
    "BM25": bm25_search,
    "Semantic": semantic_search,
    "Hybrid": hybrid_search,
}

FIELDNAMES = [
    "question_id",
    "query",
    "method",
    "rank",
    "page_number",
    "chunk_id",
    "score",
    "text",
    "relevant",
]


def main():
    parser = argparse.ArgumentParser(
        description="Compare BM25, semantic, and hybrid PDF retrieval."
    )
    parser.add_argument(
        "pdf_path",
        nargs="?",
        default=str(DEFAULT_PDF_PATH),
        help=(
            "Path to a text-based PDF. Defaults to "
            "'evaluation/Fact or Fiction.pdf'."
        ),
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of passages to retrieve per question and method (default: 5).",
    )
    args = parser.parse_args()

    if args.top_k <= 0:
        parser.error("--top-k must be greater than zero.")

    pdf_path = Path(args.pdf_path).expanduser()
    if not pdf_path.is_absolute():
        pdf_path = Path.cwd() / pdf_path

    if not pdf_path.is_file():
        parser.error(
            f"PDF file not found: {pdf_path}\n"
            "Place 'Fact or Fiction.pdf' in the evaluation folder, "
            "or provide the PDF path as an argument."
        )

    if pdf_path.suffix.lower() != ".pdf":
        parser.error("The input file must have a .pdf extension.")

    print(f"Reading PDF: {pdf_path}")
    pages = extract_pdf_text(pdf_path.read_bytes())

    if not pages:
        parser.error(
            "No extractable text was found. The PDF may be scanned or image-only."
        )

    chunks = chunk_pages(pages)
    if not chunks:
        parser.error("No searchable chunks were created from the PDF.")

    print(f"Extracted text from {len(pages)} pages.")
    print(f"Created {len(chunks)} chunks.")
    print(
        f"Evaluating {len(QUESTIONS)} questions "
        f"with up to {args.top_k} results per method."
    )

    output_rows = []

    for question_id, query in QUESTIONS:
        print(f"\n{question_id}: {query}")

        for method_name, search_function in SEARCH_METHODS.items():
            results = search_function(chunks, query, top_k=args.top_k)
            print(f"  {method_name}: {len(results)} passages")

            for rank, result in enumerate(results, start=1):
                score = result.get("rrf_score", result.get("score", ""))

                output_rows.append({
                    "question_id": question_id,
                    "query": query,
                    "method": method_name,
                    "rank": rank,
                    "page_number": result["page_number"],
                    "chunk_id": result["chunk_id"],
                    "score": score,
                    "text": result["text"].replace("\n", " ").strip(),
                    "relevant": "",
                })

    EVALUATION_DIR.mkdir(parents=True, exist_ok=True)
    output_path = EVALUATION_DIR / "retrieval_results.csv"

    with output_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"\nEvaluation results saved to: {output_path}")
    print(f"Total retrieved passages saved: {len(output_rows)}")
    print(
        "\nNext: open retrieval_results.csv and mark each passage "
        "relevant as 1 or not relevant as 0."
    )


if __name__ == "__main__":
    main()
