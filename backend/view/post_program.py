from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.core_models import TrainingProgram, User
from models.pydentic_models import ProgramSelect


async def update_program(
        user: User,
        program_title: ProgramSelect,
        db: AsyncSession
):
    '''НЕДОПИСАННАЯ ФУНКЦИЯ.'''
    t_program: TrainingProgram = await db.scalar(
        select(TrainingProgram).where(
            TrainingProgram.template_name == program_title.template_name
        )
    )
    user_tp: User = await db.scalar(
        select(User).where(
            user.training_programs == program_title.template_name
        )
    )
    if user_tp:
        raise HTTPException(
            status_code=400,
            detail="Данная программа уже выбрана."
        )

    if t_program:
        t_program.users_training_programs.append(user)
        db.add(t_program)
        await db.commit()
        return {
            "program_name": t_program.template_name,
        }
    raise HTTPException(
        status_code=400,
        detail="Выберите программу тренировок из списка - Грудь, Спина, Ноги."
    )
