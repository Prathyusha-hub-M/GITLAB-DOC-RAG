from dotenv import load_dotenv
load_dotenv()
import os

from fastapi import FastAPI
from pydantic import BaseModel
from app.pipeline import run_rag_pipeline

app=FastAPI(
    title="GitLab Handbook RAG API",
    description="Hybrid RAG system with reranking and evaluation",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    query:str

class QueryResponse(BaseModel):
    answer:str
    sources: list[str]

print("Tracing:", os.getenv("LANGCHAIN_TRACING_V2"))
print("Project:", os.getenv("LANGCHAIN_PROJECT"))

@app.get("/health")
def health_check():
    return {"status":"ok"}

@app.post("/query", response_model = QueryResponse)
def query_rag(request: QueryRequest):
    result = run_rag_pipeline(request.query)

    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }