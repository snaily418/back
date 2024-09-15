import bcrypt
from services.user_service import get_users, hot_days_update
from services.task_service import get_tasks

def verify_password(plain, hashed):
    password_byte_enc = plain.encode('utf-8')
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed)


def get_password_hash(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


def every_day_check(db):
    users = get_users(db)
    for user in users:
        for category_id in range(2):
            tasks = get_tasks(db, user, category_id)
            if all([task.checked for task in tasks if task.priority][:2:]):
                hot_days_update(db, user, True)
            else:
                hot_days_update(db, user, False)

