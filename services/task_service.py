from sqlalchemy.orm import Session
import datetime

from db import Task
import models


def create_task(db: Session, user_id: int, task: models.Task):
    new_task = Task(
        category_id=task.category_id,
        user_id=user_id,
        title=task.title,
        description=task.description,
        priority=task.priority,
        checked=task.checked,
        tags=task.tags,
        time=task.time,
        remind=task.remind,
        address=None,
        markdown=None
    )
    db.add(new_task)
    db.commit()
    return new_task


def get_tasks(db: Session, user_id: int, category_id: int):
    tasks: list = db.query(Task).filter(Task.user_id == user_id, Task.category_id == category_id).all()
    return tasks


def get_task_ext(db: Session, task_id: int):
    task: Task | None = db.query(Task).filter(Task.task_id == task_id).one_or_none()
    return task


def update_task(db: Session, task: models.Task):
    db.query(Task).filter(Task.task_id == task.task_id).update({
        Task.title: task.title,
        Task.description: task.description,
        Task.priority: task.priority,
        Task.tags: task.tags,
        Task.time: task.time,
        Task.remind: task.remind,
        Task.checked: task.checked
    })
    db.commit()
    return 1

def delete_task(db: Session, task_id: int):
    db.query(Task).filter(Task.task_id == task_id).delete()
    db.commit()
    return 1


def check_task(db: Session, task_id: int):
    db.query(Task).filter(Task.task_id == task_id).update({
        Task.checked: True
    })
    db.commit()
    return 1


def finish_tasks(db: Session, user_id: int, category_id: int):
    return db.query(Task).filter(Task.user_id == user_id, Task.category_id == category_id, Task.checked == True).all()


def get_filtered_tasks(session: Session, model, **kwargs):
    filters = []

    for key, value in kwargs.items():
        if value is not None:
            filters.append(getattr(model, key) == value)

    return session.query(model).filter(*filters).all()
