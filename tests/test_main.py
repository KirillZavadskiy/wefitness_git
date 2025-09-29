import pytest
from httpx import ASGITransport, AsyncClient

from backend.main import app
from backend.models.core_models import Base, TrainingProgram, User
from backend.view.get_token import create_access_token

from .conftest import TestingSessionLocal, client, engine


@pytest.mark.asyncio
async def test_get_main():
    response = client.get("/")
    assert response.status_code == 200, response.text


@pytest.mark.usefixtures("setup_db")
@pytest.mark.asyncio
async def test_get_users_me(setup_db):
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
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        access_token = create_access_token(
            data={"sub": "test"}, expires_delta=None
        )
        response = await ac.get(
            "/users/me/",
            headers={"Authorization": f"Bearer {access_token}"}
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_points():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost/"
    ) as ac:
        access_token = create_access_token(
            data={"sub": "test"}, expires_delta=None
        )
        response = await ac.get(
            "/points/",
            headers={"Authorization": f"Bearer {access_token}"}
        )
    assert response.status_code == 200


@pytest.mark.skip()
@pytest.mark.asyncio
async def test_select_program():
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
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        access_token = create_access_token(
            data={"sub": "test"}, expires_delta=None
        )
        response = await ac.post(
            "/programs/select",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"template_name": "test_program"}
        )
    assert response.status_code == 200
