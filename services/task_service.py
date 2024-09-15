from sqlalchemy.orm import Session

import schemas
from models import Task, Category, User
from exceptions import AccessDeniedException


def create_task(db: Session, category_id: int, data: schemas.TaskCreate, user: User):
    category = db.get(Category, category_id)

    if category.user != user:
        raise AccessDeniedException

    task = Task(
        category=category,
        title=data.title,
        description=data.description,
        priority=data.priority,
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(db: Session, user: User, category_id: int):
    category = db.get(Category, category_id)

    if category.user != user:
        raise AccessDeniedException

    return category.tasks


def update_task(db: Session, task_id: int, data: schemas.TaskUpdate):
    task = db.get(Task, task_id)

    task.title = data.title or task.title
    task.description = data.description or task.description
    task.priority = data.priority or task.priority
    task.tags = data.tags or task.tags
    task.time = data.time or task.time
    task.remind = data.remind or task.remind
    task.checked = data.checked or task.checked

    db.commit()


def delete_task(db: Session, task_id: int):
    db.delete(db.get(Task, task_id))
    db.commit()


def check_task(db: Session, task_id: int, user: User):
    task = db.get(Task, task_id)

    # if not task.category.user != user:
        # raise AccessDeniedException

    task.checked = True
    db.commit()


def get_finish_tasks(db: Session, user: User, category_id: int):
    return db.query(Task).filter(Task.user_id == user.id, Task.category_id == category_id, Task.checked == True).all()


def get_filtered_tasks(session: Session, model, **kwargs):
    filters = []

    for key, value in kwargs.items():
        if value is not None:
            filters.append(getattr(model, key) == value)

    return session.query(model).filter(*filters).all()
