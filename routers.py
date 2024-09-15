from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import models
import schemas
from auth import get_current_user
from database import get_db
from services.category_service import create_category
from services.task_service import create_task, get_tasks, get_task, check_task, get_finish_tasks
from services.user_service import create_user, update_user, freeze_count_update, update_user_preferences

api = APIRouter()


@api.get('/me')
async def me(
        db: Annotated[Session, Depends(get_db)], current_user: Annotated[models.User, Depends(get_current_user)]
) -> schemas.User:
    return current_user


@api.patch('/me')
async def updates_user(
        data: schemas.UserCreateOrUpdate,
        db: Annotated[Session, Depends(get_db)], current_user: Annotated[models.User, Depends(get_current_user)]
) -> schemas.User:
    update_user(db, data)
    return current_user

@api.post('/me')
async def creates_user(
        data: schemas.UserCreateOrUpdate,
        db: Annotated[Session, Depends(get_db)], current_user: Annotated[models.User, Depends(get_current_user)]
) -> schemas.User:
    return create_user(db, data)


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


@api.post('/categories/{id}/tasks/{task_id}')
async def new_task(
        id: int, task_id: int, task: schemas.TaskCreate,
        db: Annotated[Session, Depends(get_db)], current_user: Annotated[models.User, Depends(get_current_user)]
) -> schemas.Task:
    check_task(db, task_id)
    return get_task(db, task_id)


@api.get('/categories/{id}/tasks/finished')
async def new_task(
        id: int, task: schemas.TaskCreate,
        db: Annotated[Session, Depends(get_db)], current_user: Annotated[models.User, Depends(get_current_user)]
) -> list[schemas.Task]:
    tasks = get_finish_tasks(db, current_user, id)
    return tasks


@api.get('/shop')
async def shop(db: Annotated[Session, Depends(get_db)], current_user: Annotated[models.User, Depends(get_current_user)]
               ) -> list[schemas.User.money, schemas.User.freeze_count]:
    return [current_user.money, current_user.freeze_count]


@api.post('/shop/freeze')
async def freeze(count: int, db: Annotated[Session, Depends(get_db)],
                 current_user: Annotated[models.User, Depends(get_current_user)]) -> schemas.User.freeze_count:
    if current_user.money < 15 * count:
        return HTTPException(status_code=400, detail="Не хватает монет")
    freeze_count_update(db, current_user, count)

    return current_user.freeze_count


@api.post('/shop/custom')
async def custom(db: Annotated[Session, Depends(get_db)],
                 current_user: Annotated[models.User, Depends(get_current_user)],
                 accent: int = Query(default=0, gt=0, lt=3), background: str = "", ) \
        -> [schemas.User.accent, schemas.User.background]:
    if current_user.money < 6 * (max(0, accent - 1)) and (
            background != "" or current_user.money - 6 * (max(0, accent - 1)) < 10):
        return HTTPException(status_code=400, detail="Не хватает монет")

    update_user_preferences(db, current_user, accent, background)
    return [current_user.accent, current_user.background]
