from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth import get_current_user

import schemas
import models
from database import get_db
from services.user_service import create_category
from services.task_service import create_task, get_tasks

api = APIRouter()


@api.get('/me')
async def me(
    db: Annotated[Session, Depends(get_db)], current_user: Annotated[models.User, Depends(get_current_user)]
) -> schemas.User:
    return current_user


@api.patch('/me')
async def update_user(
    data: schemas.UserCreateOrUpdate,
    db: Annotated[Session, Depends(get_db)], current_user: Annotated[models.User, Depends(get_current_user)]
):
    pass


@api.get('/categories')
async def get_all_categories(
    db: Annotated[Session, Depends(get_db)], current_user: Annotated[models.User, Depends(get_current_user)]
):
    return current_user.categories


@api.post('/categories')
async def new_category(
    category: schemas.CategoryCreate,
    db: Annotated[Session, Depends(get_db)], current_user: Annotated[models.User, Depends(get_current_user)]
):
    category = create_category(db, current_user, category.title)
    return category


@api.post('/categories/{id}/tasks')
async def new_task(
    id: int, task: schemas.TaskCreate,
    db: Annotated[Session, Depends(get_db)], current_user: Annotated[models.User, Depends(get_current_user)]
) -> schemas.Task:
    task = create_task(db, id, task, current_user)
    return task


@api.get('/categories/{id}/tasks')
async def get_all_tasks(
    id: int,
    db: Annotated[Session, Depends(get_db)], current_user: Annotated[models.User, Depends(get_current_user)]
) -> list[schemas.Task]:
    return get_tasks(db, current_user, id)
