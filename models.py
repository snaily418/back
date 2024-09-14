from datetime import datetime, timedelta

from pydantic import BaseModel


class Preferences(BaseModel):
    accent: int | None
    background: str | None


class User(BaseModel):
    id: int
    username: str
    email: str

    preferences: Preferences


class UserCreateOrUpdate(BaseModel):
    username: str | None
    email: str | None
    password: str | None


class Task(BaseModel):
    title: str
    description: str | None

    checked: bool
    priority: bool

    tags: str | None
    time: datetime | None
    remind: timedelta | None


class TaskExt(Task):
    address: str | None
    markdown: str | None
