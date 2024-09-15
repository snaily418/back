from sqlalchemy.orm import Session

from models import Category, User


def get_category(db: Session, id: int):
    return db.query(Category).filter(Category.id == id).one_or_none()


def get_categorys(db: Session, user_id: int):
    return db.query(Category).filter(Category.user_id == user_id).all()


def create_category(db: Session, user: User, title: str):
    category = Category(title=title, user=user)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, id: int, title: str):
    db.query(Category).filter(Category.id == id).update(
        {title: title})
    db.commit()
    return 1


def delete_category(db: Session, id: int):
    db.query(Category).filter(Category.id == id).delete()
    db.commit()
    return 1
