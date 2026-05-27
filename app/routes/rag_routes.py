from fastapi import APIRouter
from rag.embedding import (
    search_documents,
    delete_embeddings,
    get_document_chunks
)
router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)

@router.post("/search")
def semantic_search(query: str):
    results = search_documents(query)
    return {
        "query": query,
        "results": results.get(
            "documents",
            []
        )
    }
@router.delete("/remove-document/{document_id}")
def remove_document(document_id: int):
    delete_embeddings(document_id)
    return {
        "message": "Embeddings removed"
    }
@router.get("/context/{document_id}")
def get_context(document_id: int):

    chunks = get_document_chunks(
        document_id
    )
    return {
        "document_id": document_id,
        "chunks": chunks
    }