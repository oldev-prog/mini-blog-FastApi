from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from app.data.database_init import async_session_factory
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.data.models import Post, User
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from app.schemas.post_schema import PostPOSTDTO, PostGETDTO
from typing import List
from app.dependencies import pagination_dep
from app.schemas.user_schema import UserGETDTO


async def get_all_posts(db: AsyncSession, pagination_params: pagination_dep) -> List[Post]:
    res = await db.execute(
        select(Post).options(
            selectinload(Post.author),
            selectinload(Post.comments),
            selectinload(Post.liked_by)
        ).limit(pagination_params.limit).offset(pagination_params.offset)
    )
    return res.scalars().all()

async def get_user_posts(user_id: int, db: AsyncSession):
    res = await db.execute(
        select(User.posts).options(selectinload(User.posts)).where(User.id == user_id)
    )
    return res.scalars().all()

async def get_one_post(id: int, db: AsyncSession) -> PostPOSTDTO:
    res = await db.execute(
        select(Post).where(Post.id == id).options(
            selectinload(Post.author),
            selectinload(Post.comments),
            selectinload(Post.liked_by)
        )
    )
    return res.scalar_one_or_none()

async def create_post(post: PostPOSTDTO, db: AsyncSession) -> PostPOSTDTO:
    new_post = Post(
        title = post.title,
        content = post.content,
        author_id = post.author_id
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

async def update_post(id: int, request: PostPOSTDTO, db: AsyncSession):
    post = await db.get(Post, id)
    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    for key, value in request.model_dump().items():
        setattr(post, key, value)
    await db.commit()
    await db.refresh(post)
    return post

async def delete_post(id: int, db: AsyncSession):
    post = await db.get(Post, id)
    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    await db.delete(post)
    await db.commit()
    return {
            'success': True,
        }


