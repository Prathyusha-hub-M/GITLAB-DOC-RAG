from __future__ import annotations

from pathlib import Path
from typing import List, Dict

import chromadb
from chromadb.config import  Settings
from sentence_transformers import SentenceTransformer

class DenseRetriever:
    def __init__(self, collection,
               embedding_model: str = "all-MiniLM-L6-v2",)-> None:
        
        self.collection = collection

        self.model = SentenceTransformer(embedding_model)

    def retrieve(self, query: str, top_k:int = 4)-> List[Dict]:
        query_embeddings = self.model.encode(query).tolist()

        results = self.collection.query(query_embeddings=query_embeddings,
                                        n_results=top_k,
                                        include=["documents","metadatas","distances"],)
        
        documents=results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        ids = results["ids"][0]


        #Converting distance to similarity and inversting lower distance to higher for hybrid search
        retrieved = []

        for doc_id, doc, meta, distance in zip(ids,documents,metadatas,distances):

            # similarity_score = 1-distance

            retrieved.append({
                "id":doc_id,
                "text":doc,
                "metadata":meta,
                "score":distance
            }
            )

        return retrieved