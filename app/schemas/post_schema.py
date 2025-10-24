from pydantic import BaseModel, Field
from typing import List

class PostPOSTDTO(BaseModel):
    title: str = Field(max_length=500)
    content: str = Field(max_length=5000)
    author_id: int

class PostGETDTO(PostPOSTDTO):
    id: int
    comments: List["CommentPOSTDTO"]|None
    liked_by: List["UserPOSTDTO"]

from app.schemas.comment_schema import CommentPOSTDTO
from app.schemas.user_schema import UserPOSTDTO

PostGETDTO.model_rebuild()