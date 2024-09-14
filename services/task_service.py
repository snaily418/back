from sqlalchemy.orm import sessionmaker

import db as bd
from models import Task


def create_task(db: sessionmaker, user_id: int, task: Task):
    ses = db()
    new_task = bd.Task(
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
