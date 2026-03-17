import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
import uuid

from app.schemas.posts import Post


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime.datetime
    posts: List[Post] = []

