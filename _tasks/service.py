from typing import Any
from .models import Task


def get_all_user_tasks(user: Any) -> list:
    """If user is authenticated, return list with all user's tasks"""
    tasks = []
    if user.is_authenticated:
        tasks = user.profile.task_set.all()
    return tasks


def get_task_by_id(id: int) -> Task:
    return Task.objects.get(id=id)


def delete_task(id: int) -> None:
    """Delete a task found by id"""
    get_task_by_id(id=id).delete()


def change_task_status(id: int) -> None:
    """Change task's status to the opposite"""
    task = get_task_by_id(id=id)
    task.status = not task.status
    task.save()
