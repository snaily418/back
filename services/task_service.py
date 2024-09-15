from sqlalchemy.orm import Session

import schemas
from models import Task, Category, User


def create_task(db: Session, category_id: int, data: schemas.TaskCreate, user: User):
    category = db.query(Category).filter(Category.id == category_id, Category.user == user).first()
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


def get_tasks(db: Session, user: int, category_id: int):
    category = db.query(Category).filter(Category.id == category_id, Category.user == user).first()
    tasks = db.query(Task).filter(Task.category == category).all()
    return tasks


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
