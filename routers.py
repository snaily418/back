from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth import get_current_user

import schemas
import models
from database import get_db
from services.user_service import create_category

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
async def get_categories(
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


@api.get('/categories/{id}/tasks')
async def get_tasks(
    db: Annotated[Session, Depends(get_db)], current_user: Annotated[models.User, Depends(get_current_user)]
) -> list[schemas.Task]:

    return []


@api.get('/task/{task_id}')
async def get_task(
    task_id: int,
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user),
) -> schemas.TaskExt:

    return
