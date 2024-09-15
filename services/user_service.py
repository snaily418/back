import datetime

from sqlalchemy.orm import Session


import schemas
from models import User, Category
from utils import get_password_hash, verify_password



def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).one_or_none()


def get_users(db: Session):
    return db.query(User).all()



def get_user_by_name(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()



def create_user(db: Session, credentials: schemas.UserCreateOrUpdate):
    user = User(username=credentials.username, email=credentials.email,
                password=get_password_hash(credentials.password))
    db.add(user)
    db.add(Category(title="Работа", permanent=True, user=user))
    db.add(Category(title="Личное", permanent=True, user=user))
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, credentials: schemas.UserCreateOrUpdate):
    db.query(User).filter(User.username == credentials.user.username).update(
        {User.email: credentials.email, User.avatar: credentials.avatar, User.money: credentials.money, User.hot_days: credentials.hot_days,
         User.first_hot_day: credentials.first_hot_day, User.freeze_count: credentials.freeze_count})
    db.commit()
    return True



def update_user_password(db: Session, user: User, old_password: str, new_password: str):
    old_hash = db.query(User).filter(User.username == user.username).one_or_none()
    if verify_password(old_password, old_hash):
        db.query(User).filter(User.username == user.username).update({User.hash: get_password_hash(new_password)})
        return True
    return {"error": "old password is wrong"}



def update_user_preferences(db: Session, user: User, accent: int | None, background: str):
    db.query(User).filter(User.username == user.username).update(
        {User.preference_accent: accent, User.preference_background: background})
    db.commit()
    return True


def delete_user(db: Session, user: User):
    db.query(User).filter(User.username == user.username).delete()
    db.commit()
    return True


def hot_days_update(db: Session, user: User, hot_days: bool):
    user = db.query(User).filter(User.username == user.username).one_or_none()
    if hot_days:
        db.query(User).filter(User.username == user.username).update({User.hot_days: User.hot_days + 1})
    else:
        if user.freeze_count != 0:
            db.query(User).filter(User.username == user.username).update(
                {User.hot_days: User.hot_days + 1, User.freeze_count: User.freeze_count - 1})
        else:
            db.query(User).filter(User.username == user.username).update(
                {User.hot_days: 0, User.first_hot_day: datetime.datetime.now()})
            return False
    if user.hot_days % 10 == 0:
        db.query(User).filter(User.username == user.username).update({User.money: User.money + 20})
    db.query(User).filter(User.username == user.username).update({User.money: User.money + 3})
    db.commit()
    return True


def freeze_count_update(db: Session, user: User, freeze_count: int):
    db.query(User).filter(User.username == user.username).update({User.freeze_count: User.freeze_count + freeze_count, User.money: User.money - (15*freeze_count)})
    db.commit()
    return True


