import datetime
from hashlib import sha256

from sqlalchemy.orm import Session

from db import User


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).one_or_none()


def create_user(db: Session, username: str, email: str, password: str):
    new_user = User(username=username,
                    email=email,
                    hash=sha256(password.encode()),
                    avatar="",
                    money=0,
                    hot_days=0,
                    first_hot_day=datetime.datetime,
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
    if old_hash == sha256(old_password.encode()):
        db.query(User).filter(User.username == username).update({User.hash: sha256(new_password.encode())})
        return True
    return {"error": "old password is wrong"}


def update_user_preferences(db: Session, username: str, accent: int | None, background: str):
    db.query(User).filter(User.username == username).update(
        {User.preference_accent: accent, User.preference_background: background})
    return True
