import datetime
# from typing import Optional

from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String, Table)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func
# from sqlalchemy.orm import Mapped


class Base(AsyncAttrs, DeclarativeBase):

    __abstract__ = True
    id = Column(Integer, primary_key=True)


user_mtm_training_table = Table(
    'user_mtm_training',
    Base.metadata,
    Column(
        'training_programs_id',
        ForeignKey('training_programs.id', ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        'users_id',
        ForeignKey('users.id', ondelete="CASCADE"),
        primary_key=True
    ),
)


# class User_mtm_TrainingProgram(Base):

#     __tablename__ = "user_mtm_training_programs"

#     training_programs_id = Column(
#         ForeignKey('training_programs.id', cascade="CASCADE"),
#         primary_key=True
#     )
#     users_id = Column(
#         ForeignKey('users.id', cascade="CASCADE"),
#         primary_key=True
#     )
#     extra_data: Mapped[Optional[str]]


class User(Base):
    """Модель пользователя."""

    __tablename__ = "users"
    username = Column(String, unique=True)
    password_hash = Column(String)
    email = Column(String)
    points = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False)
    comments = relationship("Comment", back_populates="users_comments")
    training_programs = relationship(
        "TrainingProgram",
        secondary="user_mtm_training",
        back_populates="users_training_programs",
        lazy="selectin"
    )
    progresses = relationship(
        'Progress',
        back_populates='users_progresses',
        uselist=False,
        lazy="selectin"
    )


class Comment(Base):
    """Комментарии пользователей."""

    __tablename__ = "comments"
    content = Column(String)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now() + datetime.timedelta(hours=3)
    )
    user_id = Column(Integer, ForeignKey("users.id"))
    users_comments = relationship(
        "User",
        back_populates="comments",
        lazy="selectin"
    )
    news_id = Column(Integer, ForeignKey("news.id"))
    news = relationship(
        "New",
        back_populates="comments_news",
        lazy="selectin"
    )


class New(Base):
    """Новости."""

    __tablename__ = "news"
    title = Column(String)
    comments_news = relationship(
        "Comment",
        back_populates="news",
        lazy="selectin"
    )


class TrainingProgram(Base):
    """Программа тренировок."""

    __tablename__ = "training_programs"
    template_name = Column(String)
    users_training_programs = relationship(
        "User",
        secondary="user_mtm_training",
        back_populates="training_programs",
        lazy="selectin"
    )


class Progress(Base):
    """Прогресс."""

    __tablename__ = "progresses"
    start_value = Column(Float)
    target_value = Column(Float)
    current_value = Column(Float)
    value = Column(Float, default=0)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    users_progresses = relationship(
        "User",
        back_populates="progresses",
        uselist=False,
        lazy="selectin"
    )

    change_body_program_id = Column(
        Integer, ForeignKey("change_body_programs.id")
    )
    change_body_programs = relationship(
        'ChangeBodyProgram',
        back_populates='progress_change_body',
        uselist=False,
        lazy="selectin"
    )


class ChangeBodyProgram(Base):
    """Программы по похудению и набору массы."""

    __tablename__ = "change_body_programs"
    program_name = Column(String)

    progress_change_body = relationship(
        "Progress",
        back_populates="change_body_programs",
        uselist=False,
        lazy="selectin"
    )
