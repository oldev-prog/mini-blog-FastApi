from sqlalchemy.ext.asyncio import AsyncSession
from app.data.database_init import async_session_factory
from fastapi import Depends
from pydantic import BaseModel
from typing import Annotated

async def get_session():
    async with async_session_factory() as session:
        yield session

session_dep = Annotated[AsyncSession, Depends(get_session)]

class PaginationParams(BaseModel):
    offset: int
    limit: int

pagination_dep = Annotated[PaginationParams, Depends(PaginationParams)]