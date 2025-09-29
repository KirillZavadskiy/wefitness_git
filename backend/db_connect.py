from fastapi import Request
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.settings import (POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD,
                              POSTGRES_USER)

from logging import Logger

# redis_client = redis.Redis(host='redis', port=6379, db=0)
# pool = aioredis.from_url("redis://localhost:6379/0")


engine = create_async_engine(
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"
)
SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def get_redis(request: Request):
    return request.app.state.redis


# async def get_client():
#     redis_client = aioredis.Redis(connection_pool=pool)
#     try:
#         yield redis_client
#     finally:
#         await redis_client.close()
