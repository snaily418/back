from services.task_service import get_tasks
from services.user_service import get_users, hot_days_update


def every_day_check(db):
    users = get_users(db)
    for user in users:
        for category in user.categories:
            if category.permanent:
                tasks = get_tasks(db, user, category.id)
                if all([task.checked for task in tasks if task.priority][:2:]):
                    hot_days_update(db, user, True)
                else:
                    hot_days_update(db, user, False)
