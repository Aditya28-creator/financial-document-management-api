from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)
from datetime import (
    datetime,
    timezone
)
from database.db import Base
class User(Base):
    __tablename__ = "users"
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    username = Column(
        String,
        unique=True
    )
    email = Column(
        String,
        unique=True
    )
    password = Column(String)
    role = Column(
        String,
        default="Client"
    )
class Document(Base):
    __tablename__ = "documents"
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    title = Column(String)
    company_name = Column(String)
    document_type = Column(String)
    uploaded_by = Column(String)
    file_path = Column(String)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(
            timezone.utc
        )
    )