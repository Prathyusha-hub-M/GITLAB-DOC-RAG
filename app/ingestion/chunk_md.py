from __future__ import annotations

from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

def chunk_gitlab_docs(
        docs: list[Document],
        chunk_size: int = 800,
        chunk_overlap: int =200,
        )-> list[Document]:
    header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("##","h2"),("###","h3")])

    header_chunks: list[Document] = []

    for d in docs:
        pieces = header_splitter.split_text(d.page_content)
        for p in pieces:
            merged_meta={**d.metadata, **p.metadata}

            header_chunks.append(Document(
                page_content=p.page_content,metadata=
                merged_meta
            ))

    size_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)

    return size_splitter.split_documents(header_chunks)

