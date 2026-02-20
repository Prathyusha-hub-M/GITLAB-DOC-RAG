from __future__ import annotations

from typing import List, Dict

class HybridRetriever:
    def __init__(self, dense_retriever, bm25_retriever, k: int = 60):
        self.dense = dense_retriever
        self.bm25 =bm25_retriever
        self.k = k

    def retrieve(self, query: str,
                  top_k_dense: int = 10,
                    top_k_bm25: int = 10,
                      top_k_final: int=5, )->List[Dict]:
        dense_results= self.dense.retrieve(query, top_k = top_k_dense)
        bm25_results = self.bm25.retrieve(query, top_k = top_k_bm25)

        rrf_scores={}


        # Process dense results
        for rank, result in enumerate(dense_results):
            doc_id = result["id"]

            score = 1/(self.k+rank)
            if doc_id not in rrf_scores:
                rrf_scores[doc_id] ={
                    "text": result["text"],
                    "metadata": result["metadata"],
                    "score": 0.0,
                }

            rrf_scores[doc_id]["score"] += score
        # Process BM25 results
        for rank, result in enumerate(bm25_results, start=1):
            doc_id = result["ids"]

            score = 1 / (self.k + rank)

            if doc_id not in rrf_scores:
                rrf_scores[doc_id] = {
                    "text": result["text"],
                    "metadata": result["metadata"],
                    "score": 0.0,
                }

            rrf_scores[doc_id]["score"] += score

        #Sort by final RRF score
        final_results = sorted(
           rrf_scores.values(),
           key = lambda x: x["score"],
           reverse = True,)
        
        return final_results[:top_k_final]