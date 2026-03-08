from pathlib import Path
from app.retrieval.dense import DenseRetriever

ROOT = Path(__file__).resolve().parents[1]

retriever = DenseRetriever(
    persist_dir=ROOT / "data" / "chroma",
)

query = "What is GitLab's incident escalation process?"

results = retriever.retrieve(query, top_k=4)

for i, r in enumerate(results, start=1):
    print(f"\nResult {i}")
    print(f"Score: {r['score']}")
    print(f"Section: {r['metadata']['section']}")
    print(f"File: {r['metadata']['file_path']}")
    print(f"Preview: {r['text'][:300]}...")
