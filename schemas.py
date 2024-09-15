from datetime import datetime, timedelta

from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    username: str
    email: str


class UserCreateOrUpdate(UserBase):
    password: str


class User(UserBase):
    id: int
    categories: list["Category"] = []

    preference_accent: int | None
    preference_background: str | None

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    title: str
    permanent: bool


class Category(CategoryBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    title: str
    description: str | None
    priority: bool


class Task(TaskBase):
    id: int
    checked: bool

    tags: str | None
    time: datetime | None
    remind: timedelta | None

    address: str | None
    markdown: str | None

    class Config:
        orm_mode = True


# обратная совместимость, после исправлю
TaskExt = Task
