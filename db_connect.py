from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import (POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD,
                      POSTGRES_USER)

DSN: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"
engine = create_async_engine(DSN)
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
