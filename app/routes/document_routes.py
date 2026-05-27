from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.models import Document
from utils.pdf_utils import extract_text_from_pdf
from rag.embedding import (
    store_document_embedding,
    delete_document_embeddings
)

import shutil
import os

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Upload Document
@router.post("/upload")
def upload_document(
    title: str,
    company_name: str,
    document_type: str,
    uploaded_by: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = f"uploaded_files/{file.filename}"
    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )
    new_doc = Document(
        title=title,
        company_name=company_name,
        document_type=document_type,
        uploaded_by=uploaded_by,
        file_path=file_path
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    # Extract PDF Text
    text = extract_text_from_pdf(
        file_path
    )

    # Store Embeddings
    store_document_embedding(
        new_doc.id,
        text
    )
    return {
        "message": "Document uploaded successfully"
    }
# Get All Documents
@router.get("/")
def get_documents(
    db: Session = Depends(get_db)
):
    docs = db.query(Document).all()
    result = []
    for doc in docs:

        result.append({
            "id": doc.id,
            "title": doc.title,
            "company_name": doc.company_name,
            "document_type": doc.document_type,
            "uploaded_by": doc.uploaded_by,
            "file_path": doc.file_path,
            "created_at": doc.created_at
        })

    return result

# Get Document By ID
@router.get("/{document_id}")
def get_document_by_id(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "id": document.id,
        "title": document.title,
        "company_name": document.company_name,
        "document_type": document.document_type,
        "uploaded_by": document.uploaded_by,
        "file_path": document.file_path,
        "created_at": document.created_at
    }

# Delete Document
@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()
    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    # Delete File
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    # Delete Embeddings
    delete_document_embeddings(
        document_id
    )
    # Delete DB Record
    db.delete(document)
    db.commit()
    return {
        "message": "Document deleted successfully"
    }
# Search Documents
@router.get("/search/")
def search_documents(
    company_name: str = "",
    document_type: str = "",
    db: Session = Depends(get_db)
):
    query = db.query(Document)
    if company_name:

        query = query.filter(
            Document.company_name.contains(
                company_name
            )
        )
    if document_type:
        query = query.filter(
            Document.document_type.contains(
                document_type
            )
        )
    docs = query.all()
    result = []
    for doc in docs:

        result.append({
            "id": doc.id,
            "title": doc.title,
            "company_name": doc.company_name,
            "document_type": doc.document_type,
            "uploaded_by": doc.uploaded_by,
            "file_path": doc.file_path,
            "created_at": doc.created_at
        })

    return result