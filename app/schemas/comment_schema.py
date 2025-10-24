from pydantic import BaseModel, Field


class CommentPOSTDTO(BaseModel):
    content: str = Field(max_length=500)
    author_id: int
    post_id: int


class CommentGETDTO(CommentPOSTDTO):
    id: int
    author: "UserPOSTDTO"

from app.schemas.user_schema import UserPOSTDTO

CommentGETDTO.model_rebuild()