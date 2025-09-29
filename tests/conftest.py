import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.db_connect import get_db
from backend.main import app
from backend.models.core_models import Base, TrainingProgram, User

client = TestClient(app)
DATABASE_URL = "sqlite+aiosqlite:///db.sqlite3"
engine = create_async_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


async def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        await db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
async def setup_db(scope="session"):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        async with session.begin():
            session.add_all(
                [
                    User(
                        username="test",
                        password_hash="test",
                        email="zavad93@mail.ru"
                    ), TrainingProgram(template_name="test_program"),
                ]
            )
