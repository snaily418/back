from sqlalchemy.orm import Session

import db as bd
from models import Task


def create_task(db: Session, user_id: int, task: Task):
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
    db.add(new_task)
    db.commit()
    return new_task


def get_tasks(db: Session, user_id: int, category_id: int):
    tasks: list = db.query(Task).filter(Task.user_id == user_id, Task.category_id == category_id).all()
    return tasks


def get_task_ext(db: Session, task_id: int):
    task: Task | None = db.query(Task).filter(Task.task_id == task_id).one_or_none()
    return task


def update_task(db: Session, task: Task):
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
