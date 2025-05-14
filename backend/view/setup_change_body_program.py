from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.core_models import ChangeBodyProgram, Progress, User
from backend.models.pydentic_models import ChangeBodyProgramSelect


async def setaup_change_body_program(
        program_data: ChangeBodyProgramSelect,
        db: AsyncSession,
        user: User
):
    change_body_program: ChangeBodyProgram = await db.scalar(
        select(ChangeBodyProgram).where(
            ChangeBodyProgram.program_name == program_data.program_name
        )
    )
    progress: Progress = Progress(
        start_value=0,
        target_value=0,
        current_value=0,
        value=0,
        user_id=user.id,
        change_body_program_id=change_body_program.id
    )
    db.add(progress)
    await db.commit()
    return {
        "program_name": program_data.program_name
    }
