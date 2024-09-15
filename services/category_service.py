from sqlalchemy.orm import Session

from db import Category


def get_category(db: Session, id: int):
    return db.query(Category).filter(Category.id == id).one_or_none()


def get_categorys(db: Session, user_id: int):
    return db.query(Category).filter(Category.user_id == user_id).all()


def create_category(db: Session, user_id: int, title: str):
    new_Category = Category(user_id=user_id,
                            title=title)
    db.add(new_Category)
    db.commit()
    return new_Category


def update_category(db: Session, id: int, title: str):
    db.query(Category).filter(Category.id == id).update(
        {title: title})
    db.commit()
    return 1


def delete_category(db: Session, id: int):
    db.query(Category).filter(Category.id == id).delete()
    db.commit()
    return 1
