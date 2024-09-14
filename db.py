from typing import List
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, mapped_column, relationship, Mapped
from sqlalchemy.ext.declarative import declarative_base

import config

engine = create_engine(config.DATABASE_URL)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    hash: Mapped[str]
    avatar: Mapped[str]

    money: Mapped[int]

    hot_days: Mapped[int]
    first_hot_day: Mapped[datetime]
    freeze_count: Mapped[int]

    preference_accent: Mapped[int]
    preference_background: Mapped[str]

    categories: Mapped[List["Category"]] = relationship(
        back_populates="user", cascade="all"
    )


class Category:
    __tablename__ = 'categories'

    id: Mapped[int]
    user_id: Mapped[int]
    title: Mapped[str]


class Task:
    __tablename__ = 'tasks'

    id: Mapped[int]
    category_id: Mapped[int]
    user_id: Mapped[int]

    checked: Mapped[bool]
    title: Mapped[str]
    description: Mapped[str | None]
    markdown: Mapped[str | None]
    priority: Mapped[bool]

    tags: Mapped[str | None]
    time: Mapped[datetime | None]
    address: Mapped[str | None]
    remind: Mapped[timedelta | None]

    @property
    def tag_list(self):
        return self.tags.split(",")
