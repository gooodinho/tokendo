from uuid import UUID

from django.contrib.auth.models import User
from django.db.models.query import QuerySet

from .models import Task, Project, SubTask


def get_all_user_tasks(user: User) -> QuerySet:
    tasks = user.profile.task_set.all()
    return tasks


def get_all_subtasks(task: Task) -> QuerySet:
    return SubTask.objects.filter(task=task)


def get_user_inbox_tasks(user: User) -> QuerySet:
    tasks = user.profile.task_set.filter(project=None)
    return tasks


def get_project_tasks(project: Project) -> QuerySet:
    tasks = project.task_set.all()
    return tasks


def get_all_user_projects(user: User) -> QuerySet:
    projects = user.profile.project_set.all()
    return projects


def get_task_by_id(id: UUID) -> Task:
    """Return a task found by id"""
    return Task.objects.get(id=id)


def get_subtask_by_id(id: UUID) -> SubTask:
    return SubTask.objects.get(id=id)


def get_project_by_id(id: UUID) -> Project:
    return Project.objects.get(id=id)


def delete_task(id: UUID) -> None:
    """Delete a task found by id"""
    get_task_by_id(id=id).delete()


def delete_subtask(id: UUID) -> None:
    get_subtask_by_id(id).delete()


def change_task_status(id: UUID) -> None:
    """Change task's status to the opposite"""
    task = get_task_by_id(id=id)
    task.status = not task.status
    task.save()


def change_subtask_status(id: UUID) -> SubTask:
    """Change subtask's status to the opposite"""
    subtask = get_subtask_by_id(id=id)
    subtask.status = not subtask.status
    subtask.save()
    return subtask
