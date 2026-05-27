# Financial Document Management API
A FastAPI backend project for managing financial documents with semantic search and RAG capabilities.

## Features
- JWT Authentication
- Role-Based Access Control (RBAC)
- PDF Upload
- Metadata Search
- Semantic Search
- ChromaDB Vector Storage
- Financial Document Retrieval
- Swagger API Documentation

## Tech Stack
- FastAPI
- SQLite
- SQLAlchemy
- ChromaDB
- Sentence Transformers
- PyPDF
- JWT Authentication

## Project Structure
app/
├── auth/
├── database/
├── documents/
├── models/
├── rag/
├── routes/
├── utils/
├── main.py
## Installation
```bash
pip install -r requirements.txt
```
## Run Server
```bash
uvicorn main:app --reload
```
## Swagger Documentation
Open:
```bash
http://127.0.0.1:8000/docs
```

## Main APIs
### Authentication
- POST /auth/register
- POST /auth/login

### Documents
- POST /documents/upload
- GET /documents/
- GET /documents/{id}
- DELETE /documents/{id}

### RAG
- POST /rag/search
- GET /rag/context/{id}
## Semantic Search Flow
Document → Text Extraction → Embeddings → ChromaDB → Semantic Retrieval

## Author

Aditya Karande