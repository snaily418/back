from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth import get_current_user
from db import User, get_db

from models import Task, TaskExt, User as UserO, UserCreateOrUpdate

api = APIRouter()


@api.post('/db')
async def _db(db: Annotated[Session, Depends(get_db)]):
    from auth import get_password_hash
    db.add(User(username='test', email="test@test", password=get_password_hash('test')))
    db.commit()


@api.get('/me')
async def me(
    db: Annotated[Session, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user.username


@api.patch('/me')
async def update_user(
    data: UserCreateOrUpdate,
    db: Annotated[Session, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)]
):
    pass


@api.get('/categories')
async def get_categories(
    db: Annotated[Session, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)]
):
    return []


@api.post('/categories')
async def create_category(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user),
):
    return []


@api.get('/categories/{id}/tasks')
async def get_tasks(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[Task]:

    return []


@api.get('/task/{task_id}')
async def get_task(
    task_id: int,
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user),
) -> TaskExt:

    return
