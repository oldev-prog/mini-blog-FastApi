from fastapi import APIRouter, status
from app.dependencies import session_dep
from app.data.like_crud import *
from app.data.user_crud import get_one_user
from app.schemas.like_schema import *
from typing import List
from app.message_broker.publisher import publish_email

like_router = APIRouter(
    prefix='/likes',
    tags=['likes'],
    responses={}
)

@like_router.get('/', status_code=status.HTTP_200_OK, response_model=List[LikeDTO])
async def get_all_likes(db: session_dep):
    return await get_likes(db=db)

@like_router.get('/user/{user_id}', status_code=status.HTTP_200_OK, response_model=List[LikeDTO])
async def get_user_likes(user_id: int, db: session_dep):
    return await get_like_users(user_id=user_id, db=db)

@like_router.get('/post/{post_id}', status_code=status.HTTP_200_OK, response_model=List[LikeDTO])
async def get_post_likes(post_id: int, db: session_dep):
    return await get_like_posts(post_id=post_id, db=db)

@like_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_like(like: LikeDTO, db: session_dep):
    await create(like=like, db=db)
    user = await get_one_user(like.user_id, db=db)
    user_email = user.email
    print(user_email)
    await publish_email(
        exchange_name='mini_blog',
        queue_name='likes',
        subject='New like on your post!',
        to_email=user_email,
        body=f'Your post was liked by user {user.username}!',
                        )

    return JSONResponse(
        {
            'details':'like has been successfully created'
        }
    )

@like_router.delete('/user/{user_id}/post/{post_id}', status_code=status.HTTP_200_OK)
async def delete_like(user_id:int, post_id:int, db: session_dep):
    await delete_(user_id=user_id, post_id=post_id, db=db)
    return JSONResponse(
        {
            'details':'like has been successfully deleted'
        }
    )