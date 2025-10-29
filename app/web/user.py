from fastapi import APIRouter, Depends, status
from app.data.user_crud import *
from app.dependencies import get_session, session_dep, cur_user_dep
from app.data.user_crud import get_all_users
from app.schemas.user_schema import *
from typing import List
import random
from app.message_broker.publisher import publish_email

user_router = APIRouter(
    prefix = '/users',
    tags = ['users'],
    responses = {}
)

@user_router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserGETDTO])
async def list_users(db: session_dep, cur_user: cur_user_dep):
    return await get_all_users(db)

@user_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserGETDTO)
async def get_user(id: int, db: session_dep, cur_user: cur_user_dep):
    return await get_one_user(id, db)

@user_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def _user(user: UserPOSTDTO, db: session_dep, cur_user: cur_user_dep):
    await create_user(user, db)

    user_email = user.email

    var_code = random.randint(1000, 1000000)

    await publish_email(
        exchange_name='mini_blog_login',
        queue_name='ver_codes',
        subject='Varification Code',
        to_email=user_email,
        body=f'Your account varification code: {var_code}',
    )

    return JSONResponse(
        {
            "detail": "your account has been created successfully, please check your email!"
        }
    )

@user_router.post('/activate_account', status_code=status.HTTP_200_OK)
async def activate(
        user: UserGETDTO,
        code: UserVerifyCode,
        db: session_dep,
        cur_user: cur_user_dep
):
    user = await get_one_user(user.id, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    if not user.is_firstlog:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You've already activated your account",
        )
    if code.code != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='invalid code')

    user.is_verified = True
    user.is_firstlog =False
    await db.commit()
    await db.refresh(user)

    return JSONResponse(
        {
            "details": "account confirmed sucessfully"
        }
    )

@user_router.put('/{id}', status_code=status.HTTP_201_CREATED)
async def update(id: int, request: UserPOSTDTO, db: session_dep, cur_user: cur_user_dep) -> UserGETDTO:
    await update_user(id, request, db)
    return JSONResponse(
        {
            "detail": "your account has been updated successfully, please check your email!"
        }
    )

@user_router.delete('/{id', status_code=status.HTTP_200_OK)
async def delete(id: int, db: session_dep, cur_user: cur_user_dep):
    await delete_user(id, db)
    return JSONResponse(
        {
            "detail": "your account has been deleted successfully, please check your email!"
        }
    )

