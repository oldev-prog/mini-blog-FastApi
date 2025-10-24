from fastapi import APIRouter, Depends, status
from app.data.user_crud import *
from app.dependencies import get_session, session_dep
from app.data.user_crud import get_all_users
from app.schemas.user_schema import *
from typing import List

user_router = APIRouter(
    prefix = '/users',
    tags = ['users'],
    responses = {}
)

@user_router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserGETDTO])
async def list_users(db: session_dep):
    return await get_all_users(db)

@user_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserGETDTO)
async def get_user(id: int, db: session_dep):
    return await get_one_user(id, db)

@user_router.post('/', status_code=status.HTTP_201_CREATED)
async def _user(user: UserPOSTDTO, db: session_dep):
    await create_user(user, db)
    return JSONResponse(
        {
            "detail": "your account has been created successfully, please check your email!"
        }
    )

@user_router.put('/{id}', status_code=status.HTTP_201_CREATED)
async def update(id: int, request: UserPOSTDTO, db: session_dep) -> UserGETDTO:
    await update_user(id, request, db)
    return JSONResponse(
        {
            "detail": "your account has been updated successfully, please check your email!"
        }
    )

@user_router.delete('/{id', status_code=status.HTTP_200_OK)
async def delete(id: int, db: session_dep):
    await delete_user(id, db)
    return JSONResponse(
        {
            "detail": "your account has been deleted successfully, please check your email!"
        }
    )

