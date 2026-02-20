import datetime
from fastapi import FastAPI,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel,ConfigDict
from typing import Optional
import logging
from uuid6 import uuid7
import uuid


logger = logging.Logger("coolsoc_logger")
app = FastAPI()



posts = []

class Post(BaseModel):
    model_config = ConfigDict(extra='forbid')

    id: Optional[uuid.UUID] = None
    title: str
    content: str
    published: bool=True
    rating: Optional[int] = None
    created_at: Optional[datetime.datetime] = None




@app.get("/")
def root(): 
    return { "Welcome to cool social application" }


@app.get("/posts/{id}")
async def get_post(id: uuid.UUID):
    for post in posts:
        if post["id"] == id:
            return post
        
    raise HTTPException(status_code=404 , detail=f"Post with id {id} not found")

@app.post("/posts" , status_code= status.HTTP_201_CREATED)
async def create_post(payload: Post):
    
    new_post = payload.model_dump()
    new_post["id"] = uuid7()
    new_post["created_at"] = datetime.datetime.now(datetime.timezone.utc)

    posts.append(new_post)

    return {"message" : f"new post created successfully with id {new_post["id"]}"}


@app.put("/posts/{id}")
async def update_post(id:uuid.UUID , payload: Post):
    for index,post in enumerate(posts):
        print(index)



@app.delete("/posts/{id}" , status_code= status.HTTP_200_OK)
async def delete_post(id: uuid.UUID):
    for index , post in enumerate(posts):
        if post["id"] == id:
            posts.pop(index)
            return {f"Post with ID {id} have been deleted successfully "}
    

    raise HTTPException(status_code=404 , detail=f"Post with id {id} not found")