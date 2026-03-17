import uuid
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.auth import hash_password
import app.db.models.user as models
import app.schemas.user as schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Placeholder route for users. You can add user-specific routes here (like creating a user).
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing = db.query(models.User).filter(models.User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")

    hashed = hash_password(payload.password)
    new_user = models.User(username=payload.username, password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
