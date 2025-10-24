from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from app.data.database_init import async_session_factory
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from app.data.models import Post, User, Comment, Like
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from app.schemas.comment_schema import *
from typing import List

from app.schemas.like_schema import LikeDTO


async def get_likes(db: AsyncSession) -> List[Like]:
    res = await db.execute(select(Like))
    return res.scalars().all()

async def get_like_users(user_id: int, db: AsyncSession) -> List[Like]:
    res = await db.execute(
        select(Like).where(Like.user_id == user_id)
    )
    return res.scalars().all()

async def get_like_posts(post_id: int, db: AsyncSession) -> List[Like]:
    res = await db.execute(
        select(Like).where(Like.post_id == post_id)
    )
    return res.scalars().all()

async def create(like: LikeDTO, db: AsyncSession) -> Like:
    new_like = Like(
        user_id = like.user_id,
        post_id = like.post_id

    )
    db.add(new_like)
    await db.commit()
    await db.refresh(new_like)
    return new_like

async def delete_(user_id: int, post_id: int, db: AsyncSession):
    like = await db.execute(
        delete(Like).where(Like.user_id == user_id).where(Like.post_id == post_id)
    )
    await db.commit()
    return like