from sqlalchemy.orm import Session

from models import User


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_name(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, username: str, email: str, password: str):
    pass


def update_user(db: Session, username: str | None = None):
    pass


def update_user_password(db: Session, old_password: str, new_password: str):
    pass


def update_user_preferences(db: Session, accent: int | None, background: str):
    pass
