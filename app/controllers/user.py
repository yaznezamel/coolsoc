import uuid
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
import app.db.models.user as models
import app.schemas.user as schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Placeholder route for users. You can add user-specific routes here (like creating a user).
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(payload: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(**payload.model_dump(exclude={"id", "created_at", "posts"}, exclude_unset=True))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
