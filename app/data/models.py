from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, text, ForeignKey
from app.data.base import Base
from typing import List, Annotated
from datetime import datetime

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str]

    posts: Mapped[List['Post']] = relationship(back_populates='author')
    comments: Mapped[List['Comment']] = relationship(back_populates='author')
    liked_posts: Mapped[List['Post']] = relationship(
        secondary='likes',
        back_populates='liked_by')

class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(String(5000))
    created_at: Mapped[created_at]
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    author: Mapped['User'] = relationship(back_populates='posts')
    comments: Mapped[List['Comment']] = relationship(back_populates='post')
    liked_by: Mapped[List['User']] = relationship(
        secondary='likes',
        back_populates='liked_posts')

class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[intpk]
    content: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[created_at]
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)

    author: Mapped['User'] = relationship(back_populates='comments')
    post: Mapped['Post'] = relationship(back_populates='comments')

class Like(Base):
    __tablename__ = 'likes'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id', ondelete='CASCADE'), nullable=False, primary_key=True)

