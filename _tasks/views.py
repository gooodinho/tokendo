from typing import Union

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .service import *
from .forms import *


@login_required(login_url='login')
def output_inbox_or_project_tasks_view(request, project_id: UUID = None) -> Union[Http404, HttpResponse]:
    projects = get_all_user_projects(request.user)
    context = {'projects': projects}
    if project_id is not None:
        project = get_object_or_404(Project, id=project_id)
        tasks = get_project_tasks(project)
        done_tasks_count = tasks.filter(status=True).count()
        try:
            progress = done_tasks_count/tasks.count()*100
        except ZeroDivisionError: 
            progress = 0
        context['tasks'], context['project_id'], context['done_tasks_count'], context['progress'] = tasks, project_id, done_tasks_count, progress
        return render(request, '_tasks/project_tasks.html', context)
    else:
        tasks = get_user_inbox_tasks(request.user)
        done_tasks_count = tasks.filter(status=True).count()
        try:
            progress = done_tasks_count/tasks.count()*100
        except ZeroDivisionError: 
            progress = 0
        context['tasks'], context['done_tasks_count'], context['progress'] = tasks, done_tasks_count, progress
        return render(request, '_tasks/tasks.html', context)


@login_required(login_url='login')
def create_task_view(request, project_id: UUID = None) -> Union[HttpResponseRedirect, HttpResponse]:
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            profile = request.user.profile
            task = form.save(commit=False)
            task.owner = profile
            if project_id is not None:
                task.project = get_project_by_id(project_id)
                task.save()
                return redirect("project_tasks", project_id=project_id)
            else:
                task.project = None
                task.save()
            return redirect('all_tasks')    
    return render(request, '_tasks/create.html', {"form": form, 'project_id': project_id})


@login_required(login_url='login')
def delete_task_view(request, pk: int, project_id: UUID = None) -> HttpResponseRedirect:
    delete_task(pk)
    if project_id is not None:
        return redirect("project_tasks", project_id=project_id)
    else:
        return redirect("all_tasks")


@login_required(login_url='login')
def update_task_view(request, pk: int, project_id: UUID = None) -> Union[HttpResponseRedirect, HttpResponse]:
    task = get_task_by_id(pk)
    form = TaskEditForm(request.user.profile, instance=task)
    if request.method == "POST":
        form = TaskEditForm(request.user.profile, request.POST, instance=task)
        if form.is_valid():
            form.save()
            if project_id is not None:
                return redirect("project_tasks", project_id=project_id)
            else:
                return redirect("all_tasks")
    return render(request, '_tasks/update.html', {'task': task, 'form': form, 'project_id': project_id})


@login_required(login_url='login')
def change_task_status_view(request, pk: UUID, project_id: UUID = None) -> HttpResponseRedirect:
    change_task_status(pk)
    if project_id is not None:
        return redirect("project_tasks", project_id=project_id)
    else:
        return redirect("all_tasks")


@login_required(login_url='login')
def create_project_view(request, project_id: UUID = None):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            profile = request.user.profile
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect("project_tasks", project_id=project.id)
    return render(request, '_tasks/create_project.html', {"form": form, "project_id": project_id})


@login_required(login_url='login')
def task_info_view(request, task_id: UUID, project_id: UUID = None):
    task = get_task_by_id(task_id)
    subtasks = get_all_subtasks(task)
    done_subtasks = subtasks.filter(status=True).count()
    try:
        progress = done_subtasks/subtasks.count()*100
    except ZeroDivisionError: 
        progress = 0
    return render(request, '_tasks/task_page.html', {'task': task, 'subtasks': subtasks, "project_id": project_id, 'done_subtasks_count': done_subtasks, 'progress': progress})


@login_required(login_url='login')
def create_subtask_view(request, task_id: UUID, project_id: UUID = None):
    form = SubTaskForm()
    if request.method == "POST":
        form = SubTaskForm(request.POST)
        if form.is_valid():
            subtask = form.save(commit=False)
            subtask.owner = request.user.profile
            subtask.task = get_task_by_id(task_id)
            subtask.save()
            if project_id:
                return redirect("project_task_info", project_id=project_id, task_id=task_id)
            else:
                return redirect('inbox_task_info', task_id=task_id)    
    return render(request, '_tasks/create_subtask.html', {"form": form, 'task_id': task_id, 'project_id': project_id})


@login_required(login_url='login')
def change_subtask_status_view(request, pk: UUID, project_id: UUID = None):
    subtask = change_subtask_status(pk)
    if project_id is not None:
        return redirect("project_task_info", project_id=project_id, task_id=subtask.task.id)
    else:
        return redirect("inbox_task_info", task_id=subtask.task.id)


@login_required(login_url='login')
def delete_subtask_view(request, pk: UUID, project_id: UUID = None):
    subtask = get_subtask_by_id(pk)
    delete_subtask(pk)
    if project_id is not None:
        return redirect("project_task_info", project_id=project_id, task_id=subtask.task.id)
    else:
        return redirect("inbox_task_info", task_id=subtask.task.id)


@login_required(login_url='login')
def update_subtask_view(request, pk: UUID, project_id: UUID = None):
    subtask = get_subtask_by_id(pk)
    form = SubTaskEditForm(request.user.profile, instance=subtask)
    if request.method == "POST":
        form = SubTaskEditForm(request.user.profile, request.POST, instance=subtask)
        if form.is_valid():
            form.save()
            if project_id is not None:
                return redirect("project_task_info", project_id=project_id, task_id=subtask.task.id)
            else:
                return redirect("inbox_task_info", task_id=subtask.task.id)
    return render(request, '_tasks/update_subtask.html', {'subtask': subtask, 'form': form, 'project_id': project_id})