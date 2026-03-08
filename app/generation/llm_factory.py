from langchain_ollama import ChatOllama
import os

def create_llm():
    llm = ChatOllama(
        model="llama3",
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=0,
    )

    return llm