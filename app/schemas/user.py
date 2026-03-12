import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
import uuid

from app.schemas.posts import Post


class User(BaseModel):
    model_config = ConfigDict(extra='forbid')

    id: Optional[uuid.UUID] = None
    username: str
    password: str
    created_at: Optional[datetime.datetime] = None
    posts: List[Post]

