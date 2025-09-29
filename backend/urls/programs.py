import asyncio
import json
from typing import Annotated

from redis.asyncio import Redis
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.celery_app.celery_email.tasks import send_xlxs_progress
from backend.db_connect import get_db, get_redis
from backend.models.core_models import TrainingProgram, User
from backend.models.pydantic_models import (ChangeBodyProgramSelect,
                                            ProgramSelect, ProgressUpdate)
from backend.view.get_user import get_current_user
from backend.view.post_program import update_program
from backend.view.setup_change_body_program import setaup_change_body_program
from backend.view.setup_progress import setup_progress
from backend.xlsx_app.create_xlsx import create_progress_xlsx

router = APIRouter(tags=["Main"])


@router.get("/")
async def home_page():
    return {
        "message": "Это стартовая страница",
    }


@router.get("/users/me/")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


@router.get("/points/")
async def profile(
    current_user: Annotated[User, Depends(get_current_user)],
    redis_client: Annotated[Redis, Depends(get_redis)],
):
    print(await redis_client.info())
    cash_value = await redis_client.get(f"get_points {current_user.username}")
    if cash_value:
        return json.loads(cash_value)

    await redis_client.set(
        f"get_points {current_user.username}",
        json.dumps(current_user.points),
        ex=1000
    )
    await asyncio.sleep(4)
    return current_user.points


@router.post("/programs/select", status_code=200)
async def select_program(
    current_user: Annotated[User, Depends(get_current_user)],
    template_name: ProgramSelect,
    db: AsyncSession = Depends(get_db)
):
    return await update_program(
        user=current_user,
        program_title=template_name,
        db=db
    )


@router.get("/programs/my-programs/")
async def my_programs(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    """Доработать. Выдает все программы."""
    tp_list = []
    all_tp = await db.execute(
        select(TrainingProgram).where(User.username == current_user.username)
    )
    for tp in all_tp.scalars():
        tp_list.append(tp.template_name)
    return tp_list


@router.get("/programs/")
async def all_programs(
    redis_client: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_db),
):
    cahe_value = await redis_client.get("get_programs")
    if cahe_value:
        return json.loads(cahe_value)

    tp_list = []
    all_tp = await db.execute(select(TrainingProgram))
    for tp in all_tp.scalars():
        tp_list.append(tp.template_name)

    redis_client.set("get_programs", json.dumps(tp_list))
    redis_client.expire("get_programs", 10)
    return tp_list


@router.get("/progress/")
async def progress_get(
    current_user: Annotated[User, Depends(get_current_user)],
    redis_client: Annotated[Redis, Depends(get_redis)],
):
    cahe_value = redis_client.get(f"get_progress {current_user.username}")
    if cahe_value:
        return json.loads(cahe_value)

    if current_user.progresses.value:
        redis_client.set(
            f"get_progress {current_user.username}",
            json.dumps(current_user.progresses.value)
        )
        return f"{current_user.progresses.value}%"

    raise HTTPException(
        status_code=400,
        detail="Вы не выставили цель."
    )


@router.post("/progress/")
async def progress_select(
    value: ProgressUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    return await setup_progress(value_data=value, db=db, user=current_user)


@router.post("/change-body-program/")
async def change_body_program(
    program_name: ChangeBodyProgramSelect,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    return await setaup_change_body_program(
        program_data=program_name,
        db=db,
        user=current_user
    )


@router.get("/report/generate/")
async def generate_progress(
    current_user: Annotated[User, Depends(get_current_user)]
):
    file_name = await create_progress_xlsx(user=current_user)
    send_xlxs_progress.delay(email=current_user.email, file_name=file_name)
    return {
        "response": "Прогресс отправлен на почту"
    }
