from sqlalchemy.orm import Session

import schemas
from models import User, Category
from utils import get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_name(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, credentials: schemas.UserCreateOrUpdate):
    user = User(username=credentials.username, emil=credentials.email, password=get_password_hash(credentials.password))
    db.add(user)
    db.add(Category(title="Работа", permanent=True, user=user))
    db.add(Category(title="Личное", permanent=True, user=user))
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, credentials: schemas.UserCreateOrUpdate):
    pass


def update_user_password(db: Session, old_password: str, new_password: str):
    pass


def update_user_preferences(db: Session, accent: int | None, background: str):
    pass
