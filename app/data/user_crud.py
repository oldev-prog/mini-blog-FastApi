from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from app.data.database_init import async_session_factory
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.data.models import User
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from app.schemas.user_schema import UserPOSTDTO, UserGETDTO
from typing import List
from app.utils.auth_utils import get_password_hash

new_session = async_session_factory

async def get_all_users(db: AsyncSession) -> List[User]:
    res = await db.execute(
        select(User).options(selectinload(User.posts))
    )
    return res.scalars().all()

async def get_one_user(id: int, db: AsyncSession) -> User:
    res = await db.execute(
        select(User).options(selectinload(User.posts)).where(User.id == id)
    )
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user

async def create_user(user: UserPOSTDTO, db: AsyncSession) -> User:
    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = get_password_hash(user.password),
        is_verified=False,
        is_firstlog=True
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return JSONResponse(
        {
            'success': True,
        }
    )

async def delete_user(id: int, db: AsyncSession):
    user = await db.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    await db.delete(user)
    await db.commit()
    return JSONResponse(
        {
            'success': True,
        }
    )

async def update_user(id: int, request: UserPOSTDTO, db: AsyncSession):
    user = await db.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    for key, value in request.model_dump().items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return JSONResponse(
        {
            'success': True,
        }
    )



