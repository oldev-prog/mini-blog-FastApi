from fastapi import APIRouter, status
from app.dependencies import session_dep, pagination_dep, PaginationParams
from app.data.post_crud import *
from app.schemas.post_schema import *
from typing import List

post_router = APIRouter(
    prefix = '/posts',
    tags=['posts'],
    responses={}
)

@post_router.get('/', status_code=status.HTTP_200_OK, response_model=List[PostGETDTO])
async def list_posts(db: session_dep):
    return await get_all_posts(db)

@post_router.get('/user/{user_id}')
async def list_user_posts(user_id: int, db: session_dep):
    return await get_user_posts(user_id, db)

@post_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=PostGETDTO)
async def get_post(id: int, db: session_dep):
    return await get_one_post(id, db)

@post_router.post('/', status_code=status.HTTP_201_CREATED)
async def new_post(post: PostPOSTDTO, db: session_dep):
    await create_post(post, db)
    return JSONResponse(
        {
            'detail':'your post has been created successfully, please check your account!',
        }
    )

@post_router.put('/{id}', status_code=status.HTTP_201_CREATED)
async def update_post(id: int, request: PostPOSTDTO, db: session_dep):
    await update_post(id, request, db)
    return JSONResponse(
        {
            'detail':'your post has been updated successfully, please check your account!',
        }
    )

@post_router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete(id: int, db: session_dep):
    await delete_post(id, db)
    return JSONResponse(
        {
            'detail':'your post has been deleted successfully, please check your account!',
        }
    )