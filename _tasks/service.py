from uuid import UUID
from typing import Union

from django.contrib.auth.models import User
from django.db.models.query import QuerySet

from _tasks.forms import TaskForm, ProjectForm, SubTaskForm

from .models import Task, Project, SubTask


def create_task_handler(request, next: str) -> None:
    form = TaskForm(request.POST)
    if form.is_valid():
        profile = request.user.profile
        task = form.save(commit=False)
        task.owner = profile
        if next != "/":
            task.project = get_project_by_id(next.replace('/', ''))
        else:
            task.project = None
        task.save()
    else:
        raise Exception


def create_project_handler(request) -> Union[Project, None]:
    form = ProjectForm(request.POST)
    if form.is_valid():
        profile = request.user.profile
        project = form.save(commit=False)
        project.owner = profile
        project.save()
        return project
    else:
        raise Exception


def create_subtask_handler(request, task_id: UUID) -> None:
    form = SubTaskForm(request.POST)
    if form.is_valid():
        subtask = form.save(commit=False)
        subtask.owner = request.user.profile
        subtask.task = get_task_by_id(task_id)
        subtask.save()
    else:
        raise Exception


def get_all_user_tasks(user: User) -> QuerySet:
    return user.profile.task_set.all()


def get_all_subtasks(task: Task) -> QuerySet:
    return SubTask.objects.filter(task=task)


def get_user_inbox_tasks(user: User) -> QuerySet:
    return user.profile.task_set.filter(project=None)


def get_project_tasks(project: Project) -> QuerySet:
    return project.task_set.all()


def get_all_user_projects(user: User) -> QuerySet:
    user.profile.project_set.all()
    return user.profile.project_set.all()


def get_task_by_id(id: UUID) -> Task:
    return Task.objects.get(id=id)


def get_subtask_by_id(id: UUID) -> SubTask:
    return SubTask.objects.get(id=id)


def get_project_by_id(id: UUID) -> Project:
    return Project.objects.get(id=id)


def delete_task(id: UUID) -> None:
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
