from pydantic import BaseModel, EmailStr, Field
from typing import List

class UserPOSTDTO(BaseModel):
    username: str = Field(..., max_length=30)
    email: EmailStr = Field(...)
    hashed_password: str
    is_verified: bool
    is_firstlog: bool

class UserGETDTO(UserPOSTDTO):
    id: int
    posts: List["PostPOSTDTO"]|None

class Email(BaseModel):
    email: EmailStr

class Login(EmailStr):
    password: str

class UserVerifyCode(Email):
    code: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int

class RefreshToken(BaseModel):
    refresh_token: str

from app.schemas.post_schema import PostPOSTDTO

UserGETDTO.model_rebuild()