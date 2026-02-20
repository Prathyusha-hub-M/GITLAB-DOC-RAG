from __future__ import annotations

from typing import List, Dict
from rank_bm25 import BM25Okapi

class BM25Retriever:
    def __init__(self, documents: List[str],
                metadatas: List[Dict],
                  ids: List[str]):
        self.documents = documents
        self.metadatas = metadatas
        self.ids = ids

        #Tokenize the documents
        self.tokenized_docs = [doc.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(self.tokenized_docs)

    def retrieve(self, query: str, top_k: int = 4):
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)

        #get top_k indices
        top_indices = sorted(range(len(scores)), key =lambda i: scores[i], reverse = True)[:top_k]

        results = []
        for idx in top_indices:

            results.append(
                {
                "ids":self.ids[idx],
                "text":self.documents[idx],
                "metadata":self.metadatas[idx],
                "score":scores[idx],
                }
            )

        return results
