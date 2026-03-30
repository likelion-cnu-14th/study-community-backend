from pydantic import BaseModel
from datetime import datetime

from .comment import CommentResponse


class PostCreate(BaseModel):
    title: str
    content: str
    author: str


class PostResponse(BaseModel):
    id: str
    title: str
    content: str
    author: str
    createdAt: datetime
    likes: int
    comments: list[CommentResponse]

    model_config = {"from_attributes": True}


class PostSummary(BaseModel):
    id: str
    title: str
    author: str
    createdAt: datetime
    likes: int
    commentCount: int

    model_config = {"from_attributes": True}
