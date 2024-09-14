from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import session, User

from models import Task, TaskExt, User, UserCreateOrUpdate

api = APIRouter()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def get_current_user() -> User:
    pass


@api.patch('/me')
async def update_user(
    data: UserCreateOrUpdate,
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    pass


@api.get('/categories')
async def get_categories(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
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
