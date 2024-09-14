from typing import Optional

from sqlalchemy.orm import sessionmaker

import db as bd
from models import Task


def create_task(db: sessionmaker, user_id: int, title: str, description: Optional[str] = None,
                priority: bool = False, category_id: Optional[int] = 0,
                checked: bool = False, tags: Optional[str] = None, time: Optional[str] = None,
                remind: Optional[int] = None):
    ses = db()
    new_task = bd.Task(
        category_id=category_id,
        user_id=user_id,
        title=title,
        description=description,
        markdown=None,
        priority=priority,
        checked=checked,
        tags=tags,
        time=time,
        address=None,
        remind=remind
    )
    ses.add(new_task)
    ses.commit()
    return new_task


def get_tasks(db: sessionmaker, user_id: int, category_id: int):
    ses = db()
    tasks: list = ses.query(Task).filter(Task.user_id == user_id, Task.category_id == category_id).all()
    return tasks


def get_task_ext(db: sessionmaker, task_id: int):
    ses = db()
    task: Task | None = ses.query(Task).filter(Task.task_id == task_id).one_or_none()
    return task


def update_task(db: sessionmaker, task: Task):
    ses = db()
    ses.query(Task).filter(Task.task_id == task.task_id).update({
        Task.title: task.title,
        Task.description: task.description,
        Task.priority: task.priority,
        Task.tags: task.tags,
        Task.time: task.time,
        Task.remind: task.remind,
        Task.checked: task.checked
    })
    ses.commit()
