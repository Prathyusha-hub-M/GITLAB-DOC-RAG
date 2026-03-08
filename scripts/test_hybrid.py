from pathlib import Path

from app.retrieval.dense import DenseRetriever
from app.retrieval.bm25 import BM25Retriever
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.reranker import CrossEncoderReranker
from app.generation.qa_generator import LocalQAGenerator

import chromadb
from chromadb.config import Settings
import app.retrieval.bm25
print(app.retrieval.bm25.__file__)

ROOT = Path(__file__).resolve().parents[1]

# Load dense retriever
dense = DenseRetriever(
    persist_dir=ROOT / "data" / "chroma"
)

# Load all documents from Chroma for BM25
client = chromadb.PersistentClient(
    path=str(ROOT / "data" / "chroma"),
    settings=Settings(anonymized_telemetry=False),
)

collection = client.get_collection("gitlab_handbook_mvp")

all_data = collection.get(include=["documents", "metadatas"])

bm25 = BM25Retriever(
    documents=all_data["documents"],
    metadatas=all_data["metadatas"],
    ids=all_data["ids"],
)

hybrid = HybridRetriever(dense, bm25)

query = "What is GitLab's incident escalation process?"

results = hybrid.retrieve(query)

##final results after reranking
reranker = CrossEncoderReranker()

hybrid_results = hybrid.retrieve(query, top_k_dense=10, top_k_bm25=10, top_k_final=10)

final_results = reranker.rerank(query, hybrid_results, top_k=5)

for i, r in enumerate(results, start=1):
    print(f"\nResult {i}")
    print(f"RRF Score: {r['score']}")
    print(f"Section: {r['metadata']['section']}")
    print(f"File: {r['metadata']['file_path']}")
    print(f"Preview: {r['text'][:300]}...")

print("After Reranking:")
for r in final_results:
    print(r["rerank_score"], r["metadata"]["file_path"])

#testing answer

qa = LocalQAGenerator()

# contexts = [r["text"]for r in final_results]

result = qa.generate(query, final_results)
print("\nFinal Answer:\n")
print(result["answer"])

print("\nsources:\n")
for i, src in enumerate(result["sources"], start= 1):
    print(f"{i}. {src}")