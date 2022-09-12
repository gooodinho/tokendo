from typing import Union

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .service import *
from .forms import *


def output_inbox_tasks_view(request) -> HttpResponse:
    context = {}
    if request.user.is_authenticated is True:
        projects = get_all_user_projects(request.user)
        tasks = get_user_inbox_tasks(request.user)
        done_tasks_quantity = tasks.filter(status=True).count()
        try:
            progress = done_tasks_quantity/tasks.count()*100
        except ZeroDivisionError: 
            progress = 0
        print(progress)
        context = {
            'projects': projects,
            'tasks': tasks,
            'done_tasks_quantity': done_tasks_quantity,
            'progress': progress,
        }
    return render(request, '_tasks/tasks.html', context)


@login_required(login_url='login')
def output_project_tasks_view(request, project_id: UUID) -> Union[HttpResponse, Http404]:
    projects = get_all_user_projects(request.user)
    project = get_object_or_404(Project, id=project_id)
    tasks = get_project_tasks(project)
    done_tasks_quantity = tasks.filter(status=True).count()
    try:
        progress = done_tasks_quantity/tasks.count()*100
    except ZeroDivisionError: 
        progress = 0
    context = {
        'tasks': tasks,
        'projects': projects,
        'project_id': project_id,
        'done_tasks_quantity': done_tasks_quantity,
        'progress': progress
    }
    return render(request, '_tasks/tasks.html', context)


@login_required(login_url='login')
def create_task_view(request) -> Union[HttpResponseRedirect, HttpResponse]:
    form = TaskForm()
    if request.method == "POST":
        next = request.POST.get('next', '/')
        form = TaskForm(request.POST)
        if form.is_valid():
            profile = request.user.profile
            task = form.save(commit=False)
            task.owner = profile
            task.project = None 
            if next != "/":
                task.project = get_project_by_id(next.replace('/', ''))
            task.save()
            return redirect(next)
    return render(request, '_tasks/create.html', {"form": form})


@login_required(login_url='login')
def delete_task_view(request, task_id: UUID) -> HttpResponseRedirect:
    delete_task(task_id)
    next = request.GET.get('next', '/')
    return redirect(next)


@login_required(login_url='login')
def update_task_view(request, task_id: UUID) -> Union[HttpResponseRedirect, HttpResponse]:
    task = get_task_by_id(task_id)
    form = TaskEditForm(request.user.profile, instance=task)
    if request.method == "POST":
        next = request.POST.get('next', '/')
        form = TaskEditForm(request.user.profile, request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(next)
    return render(request, '_tasks/update.html', {'task': task, 'form': form})


@login_required(login_url='login')
def change_task_status_view(request, task_id: UUID) -> HttpResponseRedirect:
    change_task_status(task_id)
    next = request.GET.get('next', '/')
    return redirect(next)

@login_required(login_url='login')
def create_project_view(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            profile = request.user.profile
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect("project_tasks", project_id=project.id)
    return render(request, '_tasks/create_project.html', {"form": form})


@login_required(login_url='login')
def task_info_view(request, task_id: UUID):
    task = get_object_or_404(Task, id=task_id)
    subtasks = get_all_subtasks(task)
    done_subtasks = subtasks.filter(status=True).count()
    try:
        progress = done_subtasks/subtasks.count()*100
    except ZeroDivisionError: 
        progress = 0
    return render(request, '_tasks/task_page.html', {'task': task, 'subtasks': subtasks, 'done_subtasks_count': done_subtasks, 'progress': progress})


@login_required(login_url='login')
def create_subtask_view(request, task_id: UUID):
    form = SubTaskForm()
    if request.method == "POST":
        next = request.POST.get('next', '/')
        form = SubTaskForm(request.POST)
        if form.is_valid():
            subtask = form.save(commit=False)
            subtask.owner = request.user.profile
            subtask.task = get_task_by_id(task_id)
            subtask.save()
            return redirect(next) 
    return render(request, '_tasks/create_subtask.html', {"form": form, 'task_id': task_id})


@login_required(login_url='login')
def change_subtask_status_view(request, subtask_id: UUID):
    change_subtask_status(subtask_id)
    next = request.GET.get('next', '/')
    return redirect(next)


@login_required(login_url='login')
def delete_subtask_view(request, subtask_id: UUID):
    get_subtask_by_id(subtask_id)
    delete_subtask(subtask_id)
    next = request.GET.get('next', '/')
    return redirect(next)

@login_required(login_url='login')
def update_subtask_view(request, subtask_id: UUID):
    subtask = get_subtask_by_id(subtask_id)
    form = SubTaskEditForm(instance=subtask)
    if request.method == "POST":
        next = request.POST.get('next', '/')
        form = SubTaskEditForm(request.POST, instance=subtask)
        if form.is_valid():
            form.save()
            return redirect(next)
    return render(request, '_tasks/update_subtask.html', {'subtask': subtask, 'form': form})