from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from models.core_models import Progress, User
from models.pydentic_models import ProgressUpdate


async def setup_progress(
        value_data: ProgressUpdate,
        db: AsyncSession,
        user: User
):
    progress: Progress = await db.scalar(
        select(Progress).where(
            Progress.user_id == user.id
        )
    )
    if progress:
        progress.start_value = value_data.start_value
        progress.target_value = value_data.target_value
        progress.current_value = value_data.current_value
        progress.value = (
            (value_data.start_value - value_data.current_value)
            / (value_data.start_value - value_data.target_value) * 100
        )
        db.add(progress)
        await db.commit()
        return {
            "change_body_program": progress.change_body_programs.program_name,
            "start_value": progress.start_value,
            "target_value": progress.target_value,
            "current_value": progress.current_value,
            "progress_value": f"{progress.value}%"
        }
    raise HTTPException(
        status_code=400,
        detail=(
            "Выберите программу по изменению тела, чтобы"
            "внести данные о вашем весе."
        )
    )
