from typing import List
from datetime import datetime, timedelta

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    avatar: Mapped[str | None]

    money: Mapped[int] = mapped_column(default=0)

    hot_days: Mapped[int] = mapped_column(default=0)
    first_hot_day: Mapped[datetime] = mapped_column(default=datetime.now)
    freeze_count: Mapped[int] = mapped_column(default=0)

    preference_accent: Mapped[int] = mapped_column(default=0)
    preference_background: Mapped[str | None]

    categories: Mapped[List["Category"]] = relationship(
        back_populates="user"
    )


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    permanent: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="categories")

    tasks: Mapped[List["Task"]] = relationship(back_populates="category")


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="tasks")

    checked: Mapped[bool] = mapped_column(default=False)
    title: Mapped[str]
    description: Mapped[str | None]
    markdown: Mapped[str | None]
    priority: Mapped[bool] = mapped_column(default=False)

    tags: Mapped[str | None]
    time: Mapped[datetime | None]
    address: Mapped[str | None]
    remind: Mapped[timedelta | None]
