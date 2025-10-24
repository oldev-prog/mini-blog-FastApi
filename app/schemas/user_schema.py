from pydantic import BaseModel, EmailStr, Field
from typing import List

class UserPOSTDTO(BaseModel):
    username: str = Field(..., max_length=30)
    email: EmailStr = Field(...)
    hashed_password: str

class UserGETDTO(UserPOSTDTO):
    id: int
    posts: List["PostPOSTDTO"]|None

from app.schemas.post_schema import PostPOSTDTO

UserGETDTO.model_rebuild()