from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.models import User
from auth.auth_handler import (
    hash_password,
    verify_password,
    create_access_token
)
from pydantic import (
    BaseModel,
    EmailStr
)
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

ROLE_PERMISSIONS = {
    "Admin": [
        "full_access"
    ],

    "Analyst": [
        "upload_documents",
        "edit_documents"
    ],

    "Auditor": [
        "review_documents"
    ],

    "Client": [
        "view_documents"
    ]
}

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()
class RegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "Client"
class RoleSchema(BaseModel):
    user_id: int
    role: str

@router.post("/register")
def register(
    payload: RegisterSchema,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == payload.email
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    if payload.role not in ROLE_PERMISSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    user = User(
        username=payload.username,
        email=payload.email,
        password=hash_password(
            payload.password
        ),
        role=payload.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "message": "User registered"
    }
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user:
       raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    valid_password = verify_password(
        form_data.password,
        user.password
    )
    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    token = create_access_token({
        "sub": user.email
    })
    return {
        "access_token": token,
        "token_type": "bearer"
    }
@router.post("/assign-role")
def assign_role(
    payload: RoleSchema,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == payload.user_id
    ).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if payload.role not in ROLE_PERMISSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )
    user.role = payload.role
    db.commit()
    return {
        "message": "Role updated"
    }
@router.get("/{user_id}/roles")
def get_user_role(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return {
        "username": user.username,
        "role": user.role
    }

@router.get("/{user_id}/permissions")
def get_permissions(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return {
        "role": user.role,
        "permissions": ROLE_PERMISSIONS.get(
            user.role,
            []
        )
    }