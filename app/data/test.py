from multiprocessing.spawn import set_executable

from models import User, Post, Comment, Like
from database_init import session_factory, async_session_factory
from sqlalchemy import select, update, delete, exists, func
from sqlalchemy.orm import selectinload, joinedload, outerjoin
from app.schemas.user_schema import UserGETDTO, UserPOSTDTO
from app.schemas.post_schema import PostPOSTDTO, PostGETDTO
from app.schemas.comment_schema import CommentPOSTDTO, CommentGETDTO
import asyncio

with session_factory() as session:
    post_id = 27
    query = select(User.username,
                   func.count(Like.user_id).label('likes'),
                   func.count(Comment.author_id).label('comments'),
                   func.count(Post.author_id).label('posts')
                   ).outerjoin(Post, Post.author_id == User.id
                    ).outerjoin(Like, Like.post_id == Post.id
                    ).outerjoin(Comment, Comment.post_id == Post.id
                                ).group_by(User.username)
    res = session.execute(query)
    res_orm = res.all()
    for row in res_orm:
        data = row._mapping
        print(f'username: {data['username']}, likes: {data['likes']}, comments: {data['comments']}, posts: {data['posts']}')

async def query1():
    async with async_session_factory() as session:
        query = select(User).options(selectinload(User.posts)).where(User.username == 'alice')
        res = await session.execute(query)
        user: User = res.scalar()
        res_dto = UserGETDTO.model_validate(user, from_attributes=True)
        print(f'user: {res_dto}')
        for post in user.posts:
            print(f'post title: {post.title}, created_at: {post.created_at}')

async def query2():
    async with async_session_factory() as session:
        query = select(Post).options(selectinload(Post.comments)).where(Post.id == 3)
        res = await session.execute(query)
        post: Post = res.scalar()
        # res_dto  = PostGETDTO.model_validate(post, from_attributes=True)
        # print(f'post: {res_dto}')
        for comment in post.comments:
            print(f'comment title: {comment.content}, created_at: {comment.created_at}')

asyncio.run(query2())