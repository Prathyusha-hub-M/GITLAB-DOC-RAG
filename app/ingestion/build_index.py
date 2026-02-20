from __future__ import annotations

from pathlib import Path
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from uuid import uuid4

from app.ingestion.load_gitlab import IngestionConfig,load_gitlab_docs
from app.ingestion.chunk_md import chunk_gitlab_docs

def build_chroma_index(cfg: IngestionConfig,
                       persist_dir: Path,
                       collection_name: str = "gitlab_handbook_mvp",
                       embedding_model: str = "all-MiniLM-L6-v2",)-> None:
    persist_dir.mkdir(parents=True, exist_ok=True)

    docs = load_gitlab_docs(cfg)
    chunks = chunk_gitlab_docs(docs)

    print(f"Loaded documents: {len(docs)}")
    print(f"Created chunks: {len(chunks)}")

    client=chromadb.PersistentClient(path=str(persist_dir),
                                     settings=Settings(anonymized_telemetry=False))
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    collection=client.get_or_create_collection(name = collection_name)
    model = SentenceTransformer(embedding_model)

    texts = [c.page_content for c in chunks]
    metadata=[c.metadata for c in chunks]
    ids= [str(uuid4()) for _ in chunks]
    
    print("Generating embeddings...")
    embeddings = model.encode(texts, batch_size=64, show_progress_bar=True).tolist()

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadata,
        ids=ids,

    )

    print(f"Stored {collection.count()} chunks in Chroma.")
    print(f"Persisted at: {persist_dir}")





