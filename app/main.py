from fastapi import FastAPI
from app.web.user import user_router
from app.web.post import post_router
from app.web.comment import comment_router
from app.web.like import like_router
from app.web.authentication import auth_router
import asyncio
from app.message_broker.consumer import consumer_main, consumer_login
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(consumer_main())
    asyncio.create_task(consumer_login())

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(like_router)
app.include_router(auth_router)