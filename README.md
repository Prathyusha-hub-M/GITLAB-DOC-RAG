# Production-Grade Hybrid RAG System

End-to-end Retrieval-Augmented Generation system built on enterprise documentation with hybrid retrieval, reranking, evaluation, observability, and API deployment.

---

## Problem

Basic RAG systems fail in production due to:

* Low recall from pure dense retrieval
* Poor precision without reranking
* Lack of evaluation
* No observability into retrieval or generation failures
* Script-based implementations with no deployment layer


---
<p align="center">
  <img src="assets/architecture.png" width="800">
</p>

## System Architecture

Data Source
→ Markdown Ingestion
→ Heading-Aware Chunking
→ Sentence-Transformer Embeddings
→ Chroma Vector Store

Query Flow:

Client
→ FastAPI
→ Hybrid Retrieval

* Dense (bi-encoder)
* BM25 (lexical)
* Reciprocal Rank Fusion
  → Cross-Encoder Reranking
  → Local LLM Generation
  → JSON Response with Citations

Observability:

* LangSmith tracing
* Stage-level latency logging
* Token usage estimation

Evaluation:

* RAGAS (faithfulness, answer relevance, context precision)

---

## Retrieval Design

### Dense Retrieval

* Sentence-Transformers bi-encoder
* Chroma persistent vector store

### Lexical Retrieval

* BM25 using rank-bm25
* Improves recall for exact policy language and technical terms

### Hybrid Fusion

* Reciprocal Rank Fusion
* Combines semantic and lexical rankings
* Reduces single-method bias

### Cross-Encoder Reranking

* ms-marco MiniLM cross-encoder
* Joint query-document scoring
* Improves precision before LLM stage


---

## Generation

* Local LLM via Ollama
* Context-grounded prompt
* Strict instruction to avoid hallucination
* Source citation extraction
* Deduplication of references

---

## Evaluation Strategy

Implemented RAGAS for:

* Faithfulness
* Answer relevance
* Context precision

Used evaluation to diagnose:

* Recall issues due to sampling
* Ranking cutoffs
* Missing corpus coverage

---

## Observability

Integrated LangSmith for:

* End-to-end trace inspection
* Retrieval span analysis
* Rerank scoring inspection
* LLM prompt visibility
* Latency per component

Also logs:

* Retrieval latency
* Rerank latency
* Generation latency
* Token estimates


---

## API Layer

FastAPI service:

POST /query

Returns:

{
"answer": "...",
"sources": [...]
}

Containerized with Docker for portability.

---

## Tech Stack

* Python
* FastAPI
* ChromaDB
* Sentence-Transformers
* rank-bm25
* Cross-encoder reranker
* Ollama
* LangSmith
* RAGAS
* Docker

---

## Engineering Decisions

* Used hybrid retrieval to balance recall and precision
* Used cross-encoder to mitigate dense retrieval semantic drift
* Used evaluation metrics to detect corpus sampling issues
* Added observability before scaling
* Separated ingestion, retrieval, reranking, generation modules for maintainability

---


