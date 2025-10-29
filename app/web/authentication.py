from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import session_dep
from app.utils.auth_utils import authenticate_user
from app.utils.auth_handler import create_refresh_token, create_access_token, verify_refresh_token
from app.schemas.user_schema import RefreshToken

auth_router = APIRouter()

@auth_router.post('/login')
async def login(
        request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = session_dep
):
    user = await authenticate_user(request, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})

    return JSONResponse(
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
        status_code=status.HTTP_200_OK,
    )

@auth_router.post("/refresh")
async def refresh(request: RefreshToken, db: AsyncSession = session_dep):
    user_id = verify_refresh_token(request.refresh_token)
    access_token = create_access_token(data={"sub": user_id})

    return JSONResponse({"access": access_token}, status_code=status.HTTP_201_CREATED)
