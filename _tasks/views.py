from typing import Union

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
        try:
            create_task_handler(request, next)
            messages.success(request, "Task was successfully created!")
            return redirect(next)
        except Exception:
            messages.warning(request, "Form data are not correct")
    return render(request, '_tasks/create.html', {"form": form})


@login_required(login_url='login')
def delete_task_view(request, task_id: UUID) -> HttpResponseRedirect:
    delete_task(task_id)
    next = request.GET.get('next', '/')
    messages.success(request, "Task was successfully deleted!")
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
            messages.success(request, "Task was successfully updated!")
            return redirect(next)
        else:
            messages.warning(request, "Form data are not correct")
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
        try:
            project = create_project_handler(request)
            messages.success(request, "Project was successfully created!")
            return redirect("project_tasks", project_id=project.id)
        except Exception:
            messages.warning(request, "Form data are not correct")
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
        try:
            create_subtask_handler(request, task_id)
            messages.success(request, "Subtask was successfully created!")
            return redirect(next)
        except Exception:
            messages.warning(request, "Form data are not correct")
    return render(request, '_tasks/create_subtask.html', {"form": form, 'task_id': task_id})


@login_required(login_url='login')
def change_subtask_status_view(request, subtask_id: UUID):
    change_subtask_status(subtask_id)
    next = request.GET.get('next', '/')
    return redirect(next)


@login_required(login_url='login')
def delete_subtask_view(request, subtask_id: UUID):
    delete_subtask(subtask_id)
    next = request.GET.get('next', '/')
    messages.success(request, "Subtask was successfully deleted!")
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