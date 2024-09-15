from datetime import datetime, timedelta

from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Preferences(BaseModel):
    accent: int | None
    background: str | None


class UserBase(BaseModel):
    username: str
    email: str


class UserCreateOrUpdate(UserBase):
    password: str


class User(UserBase):
    id: int

    preferences: Preferences

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    title: str


class Category(CategoryBase):
    id: int

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


# обратная совместимость, после мерджа исправлю
TaskExt = Task
