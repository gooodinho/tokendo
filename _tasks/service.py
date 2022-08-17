from typing import Union
from uuid import UUID

from django.contrib.auth.models import User
from django.db.models.query import QuerySet

from .models import Task, Project
from users.models import Profile


def get_all_user_tasks(user: User) -> Union[list, QuerySet]:
    """If user is authenticated, return Queryset with all user's tasks. Else return empty list."""
    tasks = []
    if user.is_authenticated:
        tasks = user.profile.task_set.all()
    return tasks


def get_user_inbox_tasks(user: User):
    tasks = []
    if user.is_authenticated:
        tasks = user.profile.task_set.filter(project=None)
    return tasks


def get_project_tasks(project: Project):
    tasks = project.task_set.all()
    return tasks


def get_all_user_projects(user: User) -> Union[list, QuerySet]:
    """If user is authenticated, return Queryset with all user's projects. Else return empty list."""
    projects = []
    if user.is_authenticated:
        projects = user.profile.project_set.all()
    return projects


def get_task_by_id(id: UUID) -> Task:
    """Return a task found by id"""
    return Task.objects.get(id=id)


def get_project_by_id(id: UUID):
    return Project.objects.get(id=id)


def delete_task(id: UUID) -> None:
    """Delete a task found by id"""
    get_task_by_id(id=id).delete()


def change_task_status(id: UUID) -> None:
    """Change task's status to the opposite"""
    task = get_task_by_id(id=id)
    task.status = not task.status
    task.save()
