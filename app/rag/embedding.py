from sentence_transformers import SentenceTransformer
import chromadb
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.get_or_create_collection(
    name="financial_docs"
)
# basic chunking for now
def split_text(text, chunk_size=400):
    chunks = []
    for i in range(0, len(text), chunk_size):
        part = text[i:i + chunk_size]
        chunks.append(part)
    return chunks
def save_embeddings(doc_id, text):
    chunks = split_text(text)
    for index, chunk in enumerate(chunks):
        vector = model.encode(chunk).tolist()
        collection.add(
            ids=[f"{doc_id}_{index}"],
            embeddings=[vector],
            documents=[chunk]
        )
def search_documents(query):
    query_vector = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=5
    )
    return results
def delete_embeddings(doc_id):
    data = collection.get()
    delete_ids = []
    for item_id in data["ids"]:
        if item_id.startswith(str(doc_id)):
            delete_ids.append(item_id)
    if delete_ids:
        collection.delete(ids=delete_ids)
def get_document_chunks(doc_id):
    data = collection.get()
    related_chunks = []
    for index, item_id in enumerate(data["ids"]):
        if item_id.startswith(str(doc_id)):
            related_chunks.append(
                data["documents"][index]
            )
    return related_chunks