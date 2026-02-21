import ollama
from typing import List, Dict

class LocalQAGenerator:
    def __init__(self, model: str="llama3"):
        self.model = model
    
    def generate(self, query: str, contexts: List[Dict])-> Dict:
        context_block =[r["text"] for r in contexts]
        sources = list([r["metadata"]["file_path"] for r in contexts])

        prompt =f'''
You ara a chat asssistant for Gitlab handbook.
Based on the provided context answer the question.
Do not answer anything out of the context, if the context does not have answer to the question say so.

context:
{context_block}

question:
{query}'''
        
        response = ollama.chat(model = self.model,
                               messages=[{"role":"user","content":prompt}]
        )
        answer = response["message"]["content"]

        return {
            "answer":answer,
            "sources":sources,
            "contexts":[c["text"] for c in contexts]
        }