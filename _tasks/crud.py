from typing import Any
from django.contrib.auth.models import User
from .models import Task


def get_all_user_tasks(user: Any) -> list:
    """If user is authenticated, return list with all user's tasks"""
    tasks = []
    if user.is_authenticated:
        tasks = User.objects.get(username=user.username).task_set.all()
    return tasks


def get_task_by_id(id: int) -> Task:
    return Task.objects.get(id=id)


def create_task(task_name: str, owner: User) -> None:
    """Create a new task for user as owner"""
    Task.objects.create(task_name=task_name, owner=owner)


def delete_task(id: int) -> None:
    """Delete a task found by id"""
    get_task_by_id(id=id).delete()


def update_task(id: int, task_name: str, task_status: bool) -> None:
    """Update a task found by id"""
    task = get_task_by_id(id=id)
    task.task_name = task_name
    task.status = task_status
    task.save()


def change_task_status(id: int) -> None:
    """Change task's status to the opposite"""
    task = get_task_by_id(id=id)
    task.status = not task.status
    task.save()
