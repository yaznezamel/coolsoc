import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
import uuid

class Post(BaseModel):
    model_config = ConfigDict(extra='forbid')

    id: Optional[uuid.UUID] = None
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
