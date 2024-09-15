from services.user_service import get_users, hot_days_update
from services.task_service import get_tasks

def every_day_check(db):
    users = get_users(db)
    for user in users:
        for category_id in range(2):
            tasks = get_tasks(db, user, category_id)
            if all([task.checked for task in tasks if task.priority][:2:]):
                hot_days_update(db, user, True)
            else:
                hot_days_update(db, user, False)