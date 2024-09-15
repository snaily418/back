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


def get_tasks(db: Session, user: User, category_id: int):
    category = db.query(Category).filter(Category.id == category_id, Category.user == user).first()
    tasks = db.query(Task).filter(Task.category == category).all()
    return tasks


def get_task(db: Session, task_id: int):
    tasks = db.query(Task).filter(Task.task_id == task_id).one_or_none()
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


def get_finish_tasks(db: Session, user: User, category_id: int):
    return db.query(Task).filter(Task.user_id == user.id, Task.category_id == category_id, Task.checked == True).all()


def get_filtered_tasks(session: Session, model, **kwargs):
    filters = []

    for key, value in kwargs.items():
        if value is not None:
            filters.append(getattr(model, key) == value)

    return session.query(model).filter(*filters).all()
