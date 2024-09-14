from typing import List
from datetime import datetime, timedelta

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, mapped_column, relationship, Mapped
from sqlalchemy.ext.declarative import declarative_base

import config

engine = create_engine(config.DATABASE_URL)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    avatar: Mapped[str | None]

    money: Mapped[int] = mapped_column(default=0)

    hot_days: Mapped[int] = mapped_column(default=0)
    first_hot_day: Mapped[datetime] = mapped_column(default=datetime.now)
    freeze_count: Mapped[int] = mapped_column(default=0)

    preference_accent: Mapped[int] = mapped_column(default=0)
    preference_background: Mapped[str | None]

    categories: Mapped[List["Category"]] = relationship(
        back_populates="user", cascade="all"
    )


class Category:
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    permanent: bool = mapped_column(default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="categories")

    tasks: Mapped[List["Task"]] = relationship()


class Task:
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    checked: Mapped[bool] = mapped_column(default=False)
    title: Mapped[str]
    description: Mapped[str | None]
    markdown: Mapped[str | None]
    priority: Mapped[bool] = mapped_column(default=False)

    tags: Mapped[str | None]
    time: Mapped[datetime | None]
    address: Mapped[str | None]
    remind: Mapped[timedelta | None]
