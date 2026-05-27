from fastapi import APIRouter

from rag.embedding import (
    search_similar_documents,
    delete_document_embeddings
)

import chromadb
from chromadb.config import Settings

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)

# ChromaDB
client = chromadb.Client(
    Settings(anonymized_telemetry=False)
)

collection = client.get_or_create_collection(
    name="financial_documents"
)


# Semantic Search
@router.post("/search")
def semantic_search(query: str):

    results = search_similar_documents(
        query
    )

    return {
        "query": query,
        "results": results
    }


# Get Context
@router.get("/context/{document_id}")
def get_document_context(
    document_id: int
):

    results = collection.get()

    chunks = []

    for i, metadata in enumerate(
        results["metadatas"]
    ):

        if metadata["document_id"] == document_id:

            chunks.append({
                "chunk": results["documents"][i],
                "metadata": metadata
            })

    return {
        "document_id": document_id,
        "chunks": chunks
    }


# Remove Embeddings
@router.delete("/remove-document/{document_id}")
def remove_document_embeddings(
    document_id: int
):

    delete_document_embeddings(
        document_id
    )

    return {
        "message": "Document embeddings removed"
    }