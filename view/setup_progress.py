from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
            abs(value_data.start_value - value_data.current_value)
            / abs(value_data.start_value - value_data.target_value) * 100
        )
        if progress.change_body_program_id == 1 and value_data.start_value < value_data.target_value:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Выбранная программа - Похудение."
                    "Стартовый вес должен быть выше цели."
                )
            )
        if progress.change_body_program_id == 2 and value_data.start_value > value_data.target_value:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Выбранная программа - Набор массы."
                    "Стартовый вес должен быть ниже цели."
                )
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
