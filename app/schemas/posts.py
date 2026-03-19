import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
import uuid

class PostBase(BaseModel):
    model_config = ConfigDict(extra='forbid')

    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime.datetime
    owner_id: uuid.UUID
