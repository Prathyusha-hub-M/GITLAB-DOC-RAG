from langsmith import traceable
from dotenv import load_dotenv

from pathlib import Path
import chromadb

from app.retrieval.dense import DenseRetriever
from app.retrieval.bm25 import BM25Retriever
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.reranker import CrossEncoderReranker
from app.generation.qa_generator import LocalQAGenerator

load_dotenv()

CHROMA_PATH = Path("data/chroma")
COLLECTION_NAME = "gitlab_handbook_mvp"


client = chromadb.PersistentClient(path=str(CHROMA_PATH))
collection = client.get_collection(COLLECTION_NAME)

all_data = collection.get(include=["documents", "metadatas"])

documents = all_data["documents"]
metadatas = all_data["metadatas"]
ids = all_data["ids"]




dense = DenseRetriever(
    collection=collection
)

bm25 = BM25Retriever(
    documents=documents,
    metadatas=metadatas,
    ids=ids)

hybrid = HybridRetriever(
    dense_retriever=dense,
    bm25_retriever=bm25
)

reranker = CrossEncoderReranker()

generator = LocalQAGenerator()


# Main Pipeline #

@traceable(name="run_rag_pipeline")
def run_rag_pipeline(query: str) -> dict:

    # Hybrid Retrieval
    hybrid_results = hybrid.retrieve(
        query,
        top_k_dense=10,
        top_k_bm25=10,
        top_k_final=10
    )

    # Cross-Encoder Rerank
    final_results = reranker.rerank(
        query,
        hybrid_results,
        top_k=5
    )

    # Generate Answer with Citations
    result = generator.generate(query, final_results)

    return result
