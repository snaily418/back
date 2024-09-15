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


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    user_id: int
    permanent: bool

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    title: str
    description: str | None
    priority: bool


class TaskCreate(TaskBase):
    pass


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
