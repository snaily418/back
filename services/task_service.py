from sqlalchemy.orm import Session
from models import Task


def create_task(db: Session, title: str):
    pass


def get_tasks(db: Session, user_id: int, category_id: int):
    pass


def get_task_ext(db: Session, task_id: int):
    pass


def update_task(db: Session, task: Task):
    pass
