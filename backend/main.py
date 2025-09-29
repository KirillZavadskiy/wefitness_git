from contextlib import asynccontextmanager
# from fastapi_admin.app import app as admin_app

from fastapi import FastAPI
from redis.asyncio import Redis

from .urls.auth import auth_router
from .urls.programs import router as programs_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = await Redis.from_url("redis://redis:6379/2")
    yield
    await app.state.redis.aclose()


app = FastAPI(lifespan=lifespan)

app.include_router(router=programs_router)
app.include_router(router=auth_router)
# app.mount("/admin", admin_app)
