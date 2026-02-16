from __future__ import annotations

from pathlib import Path
from typing import List
import random

from pydantic import BaseModel, Field, field_validator
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader, TextLoader


RANDOM_SEED = 42

class IngestionConfig(BaseModel):
    people_dir: Path
    security_dir: Path
    people_limit: int = Field(default=30, ge=1, le=2000)
    security_limit: int = Field(default=70,ge=1,le=5000)

    @field_validator("people_dir","security_dir")
    @classmethod
    def path_must_exist(cls, v:Path) -> Path:
        if not v.exists():
            raise ValueError(f"Path does not exist:{v}")
        if not v.is_dir():
            raise ValueError(f"Path is not a directory:{v}")
        return v
    
def strip_frontmatter(text: str)-> str:
    if text.startswith("---"):
        parts = text.split("\n---",1)
        if len(parts)==2:
         return parts[1].lstrip("\n")
    return text
        
def _load_dir(dir_path: Path, section: str)-> List[Document]:
    loader = DirectoryLoader(
        str(dir_path),
        glob="**/*.md",
        loader_cls = TextLoader,
        loader_kwargs={"encoding":"utf-8"},
        use_multithreading=True,
        show_progress=True,
    )
    docs = loader.load()

    out: List[Document] = []

    for d in docs:
        cleaned = strip_frontmatter(d.page_content).strip()
        if not cleaned:
            continue

        file_path = d.metadata.get("source","")
        out.append(Document(page_content = cleaned,
                            metadata={
                                "source":"gitlab_hamdbook",
                                "section":section,
                                "file_path": str(file_path).replace("\\","/"),
                                }
                            )
                        )
    return out
    
def _sample(docs: List[Document], limit: int) -> List[Document]:
        if len(docs) <= limit:
            return docs
        rng = random.Random(RANDOM_SEED)
        idxs = list(range(len(docs)))
        rng.shuffle(idxs)
        chosen = idxs[:limit]
        return [docs[i] for i in chosen]


def load_gitlab_docs(cfg: IngestionConfig) -> List[Document]:
    people_docs = _load_dir(cfg.people_dir, section="people-group")
    security_docs = _load_dir(cfg.security_dir, section="security")

    people_docs = _sample(people_docs, cfg.people_limit)
    security_docs = _sample(security_docs, cfg.security_limit)

    return people_docs + security_docs