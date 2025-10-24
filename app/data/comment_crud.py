from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from app.data.database_init import async_session_factory
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.data.models import Post, User, Comment
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from app.schemas.comment_schema import *
from typing import List

async def get_all_comments(db: AsyncSession) -> List[Comment]:
    res = await db.execute(
        select(Comment).options(selectinload(Comment.author), selectinload(Comment.post))
    )
    res = res.scalars().all()
    # res_dto = CommentGETDTO.model_validate(res, from_attributes=True)
    # print(res_dto)
    return res

async def get_one_comment(id: int, db: AsyncSession) -> Comment:
    res = await db.execute(
        select(Comment).options(selectinload(Comment.author), selectinload(Comment.post)).where(Comment.id == id)
    )
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return res.scalar_one_or_none()

async def get_user_comments(user_id: int, db: AsyncSession) -> List[Comment]:
    res = await db.execute(select(Comment).options(
            selectinload(Comment.author),
            selectinload(Comment.post)
        ).where(Comment.author_id == user_id)
    )
    res = res.scalars().all()
    print(res)
    return res

async def get_post_comments(post_id: int, db: AsyncSession) -> List[Comment]:
    res = await db.execute(
        select(Comment).where(Comment.post_id == post_id).options(
            selectinload(Comment.author),
            selectinload(Comment.post))
        )
    return res.scalars().all()

async def create(comment: CommentPOSTDTO, db: AsyncSession) -> Comment:
    new_comment = Comment(
        content=comment.content,
        author_id=comment.author_id,
        post_id=comment.post_id
    )
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment

async def update(id: int, request: CommentPOSTDTO, db: AsyncSession) -> Comment:
    comment = await db.get(Comment, id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    for key, value in request.model_dump().items():
        setattr(comment, key, value)
    await db.commit()
    await db.refresh(comment)
    return comment

async def delete(id: int, db: AsyncSession):
    comment = await db.get(Comment, id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    await db.delete(comment)
    await db.commit()
    return {'success': True}
