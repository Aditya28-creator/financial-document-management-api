from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# Load Model
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# ChromaDB Setup
client = chromadb.Client(
    Settings(anonymized_telemetry=False)
)

collection = client.get_or_create_collection(
    name="financial_documents"
)


# Split Text Into Chunks
def split_text_into_chunks(
    text,
    chunk_size=500
):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunk = text[i:i + chunk_size]

        chunks.append(chunk)

    return chunks


# Store Embeddings
def store_document_embedding(
    document_id,
    text
):

    chunks = split_text_into_chunks(
        text
    )

    for index, chunk in enumerate(chunks):

        embedding = model.encode(
            chunk
        ).tolist()

        collection.add(
            ids=[f"{document_id}_{index}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[
                {
                    "document_id": document_id,
                    "chunk_index": index
                }
            ]
        )


# Semantic Search + Simple Reranking
def search_similar_documents(query):

    query_embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=10
    )

    reranked_results = []

    documents = results["documents"][0]

    distances = results["distances"][0]

    metadatas = results["metadatas"][0]

    for i in range(len(documents)):

        reranked_results.append({
            "document": documents[i],
            "distance": distances[i],
            "metadata": metadatas[i]
        })

    # Lower distance = better match
    reranked_results = sorted(
        reranked_results,
        key=lambda x: x["distance"]
    )

    # Return Top 5
    return reranked_results[:5]


# Delete Embeddings
def delete_document_embeddings(
    document_id
):

    results = collection.get()

    ids_to_delete = []

    for i, metadata in enumerate(
        results["metadatas"]
    ):

        if metadata["document_id"] == document_id:

            ids_to_delete.append(
                results["ids"][i]
            )

    if ids_to_delete:

        collection.delete(
            ids=ids_to_delete
        )