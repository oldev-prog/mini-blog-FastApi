from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from app.data.comment_crud import *
from app.data.user_crud import get_one_user
from app.dependencies import session_dep, cur_user_dep
from app.schemas.comment_schema import *
from typing import List
from app.message_broker.publisher import publish_email

comment_router = APIRouter(
    prefix='/comments',
    tags=['comments'],
    responses={})

@comment_router.get('/', status_code=status.HTTP_200_OK, response_model=List[CommentGETDTO])
async def get_comments(db: session_dep, cur_user: cur_user_dep):
    return await get_all_comments(db)

@comment_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=CommentGETDTO)
async def get_comment(id: int, db: session_dep, cur_user: cur_user_dep):
    return await get_one_comment(id, db)

@comment_router.get('/user/{user_id}', status_code=status.HTTP_200_OK, response_model=List[CommentGETDTO])
async def user_comments(user_id: int, db: session_dep, cur_user: cur_user_dep):
    return await get_user_comments(user_id, db)

@comment_router.get('/post/{post_id}', status_code=status.HTTP_200_OK, response_model=List[CommentGETDTO])
async def post_comments(post_id: int, db: session_dep, cur_user: cur_user_dep):
    return await get_post_comments(post_id, db)

@comment_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_comment(comment: CommentPOSTDTO, db: session_dep, cur_user: cur_user_dep):
    await create(comment, db)
    user = await get_one_user(comment.author_id, db)
    user_email = user.email
    await publish_email(
        exchange_name='mini_blog',
        queue_name='comments',
        subject='New comment on your post!',
        to_email=user_email,
        body=f'Your post was commented by user {user.username}!',
    )
    return JSONResponse(
        {
            'details':'comment has been successfully created',
        }
    )

@comment_router.put('/{id}', status_code=status.HTTP_201_CREATED)
async def update_comment(id:int, data: CommentPOSTDTO, db: session_dep, cur_user: cur_user_dep):
    await update(id, data, db)
    return JSONResponse(
        {
            'details':'comment has been successfully updated',
        }
    )

@comment_router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_comment(id:int, db: session_dep, cur_user: cur_user_dep):
    await delete(id, db)
    return JSONResponse(
        {
            'details':'comment has been successfully deleted',
        }
    )