from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.core_models import TrainingProgram, User
from models.pydentic_models import ProgramSelect


async def post_program(
        user: User,
        program_title: ProgramSelect,
        db: AsyncSession
):
    '''НЕДОПИСАННАЯ ФУНКЦИЯ.'''
    tp: TrainingProgram = await db.scalar(
        select(TrainingProgram).where(
            TrainingProgram.template_name == program_title.template_name
        )
    )
    utp: User = await db.scalar(
        select(User).where(
            user.training_programs == program_title.template_name
        )
    )
    if tp and utp:
        #
        #
        #
        await db.commit()
        return {
            "id": user.id,
            "username": user.username
        }
    return False
