import datetime
from fastapi import FastAPI, status, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
import uuid

import app.models.post as models
import app.schemas.posts as schemas
from app.db.database import get_db, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root(): 
    return {"message": "Welcome to cool social application"}

@app.get("/posts", response_model=List[schemas.Post])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: uuid.UUID, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    return post

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(payload: schemas.Post, db: Session = Depends(get_db)):
    new_post = models.Post(**payload.model_dump(exclude={"id", "created_at"}, exclude_unset=True))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: uuid.UUID, payload: schemas.Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
        
    post_query.update(payload.model_dump(exclude={"id", "created_at"}, exclude_unset=True), synchronize_session=False)
    db.commit()
    
    return post_query.first()

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: uuid.UUID, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
        
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return