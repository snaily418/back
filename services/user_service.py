import datetime

from sqlalchemy.orm import Session

from db import User
from utils import verify_password, get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).one_or_none()


def get_users(db: Session, user_id: int):
    return db.query(User).all()


def create_user(db: Session, username: str, email: str, password: str):
    new_user = User(username=username,
                    email=email,
                    hash=get_password_hash(password),
                    avatar="",
                    money=0,
                    hot_days=0,
                    first_hot_day=datetime.datetime.now(),
                    freeze_count=0,
                    preference_accent=0,
                    preference_background=""
                    )
    db.add(new_user)
    db.commit()
    return new_user


def update_user(db: Session, username: str, email: str, hash: str, avatar: str, money: int, hot_days: int,
                first_hot_day: datetime, freeze_count: int, preference_accent: int, preference_background: str):
    db.query(User).filter(User.username == username).update(
        {User.email: email, User.avatar: avatar, User.money: money, User.hot_days: hot_days,
         User.first_hot_day: first_hot_day, User.freeze_count: freeze_count})
    db.commit()
    return True


def update_user_password(db: Session, username: str, old_password: str, new_password: str):
    old_hash = db.query(User).filter(User.username == username).one_or_none()
    if verify_password(old_password, old_hash):
        db.query(User).filter(User.username == username).update({User.hash: get_password_hash(new_password)})
        return True
    return {"error": "old password is wrong"}


def update_user_preferences(db: Session, username: str, accent: int | None, background: str):
    db.query(User).filter(User.username == username).update(
        {User.preference_accent: accent, User.preference_background: background})
    db.commit()
    return True


def delete_user(db: Session, username: str):
    db.query(User).filter(User.username == username).delete()
    db.commit()
    return True


def hot_days_update(db: Session, username: str, hot_days: bool):
    user = db.query(User).filter(User.username == username).one_or_none()
    if hot_days:
        db.query(User).filter(User.username == username).update({User.hot_days: User.hot_days + 1})
    else:
        if user.freeze_count != 0:
            db.query(User).filter(User.username == username).update(
                {User.hot_days: User.hot_days + 1, User.freeze_count: User.freeze_count - 1})
        else:
            db.query(User).filter(User.username == username).update(
                {User.hot_days: 0, User.first_hot_day: datetime.datetime.now()})
            return False
    if user.hot_days % 10 == 0:
        db.query(User).filter(User.username == username).update({User.money: User.money + 20})
    db.query(User).filter(User.username == username).update({User.money: User.money + 3})
    db.commit()
    return True


def freeze_count_update(db: Session, username: str, freeze_count: int):
    db.query(User).filter(User.username == username).update({User.freeze_count: User.freeze_count + freeze_count})
    db.commit()
    return True
