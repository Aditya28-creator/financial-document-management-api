from fastapi import FastAPI
from database.db import engine
from models.models import Base
from routes.auth_routes import router as auth_router
from routes.document_routes import router as document_router
from routes.rag_routes import router as rag_router
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Financial Document Management API"
)
app.include_router(auth_router)
app.include_router(document_router)
app.include_router(rag_router)
@app.get("/")
def home():
    return {
        "message": "API is running"
    }