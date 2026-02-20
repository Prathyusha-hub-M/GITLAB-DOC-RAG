from __future__ import annotations

from typing import List, Dict
from sentence_transformers import CrossEncoder


class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, candidates: List[Dict], top_k: int = 5) -> List[Dict]:

        pairs = [(query, doc["text"]) for doc in candidates]

        scores = self.model.predict(pairs)

        for doc, score in zip(candidates, scores):
            doc["rerank_score"] = float(score)

        reranked = sorted(
            candidates,
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return reranked[:top_k]