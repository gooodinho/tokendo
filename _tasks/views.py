from typing import Union

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .service import *
from .forms import TaskForm, TaskEditForm


@login_required(login_url='login')
def output_inbox_or_project_tasks_view(request, project_id: UUID = None) -> Union[Http404, HttpResponse]:
    projects = get_all_user_projects(request.user)
    context = {'projects': projects}
    if project_id is not None:
        project = get_object_or_404(Project, id=project_id)
        tasks = get_project_tasks(project)
        context['tasks'], context['project_id'] = tasks, project_id
        return render(request, '_tasks/project_tasks.html', context)
    else:
        tasks = get_user_inbox_tasks(request.user)
        context['tasks'] = tasks
        return render(request, '_tasks/tasks.html', context)


@login_required(login_url='login')
def create_task_view(request, project_id: UUID = None) -> Union[HttpResponseRedirect, HttpResponse]:
    form = TaskForm()
    print(f'Project id: {project_id}')
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            profile = request.user.profile
            task = form.save(commit=False)
            task.owner = profile
            if project_id is not None:
                task.project = get_project_by_id(project_id)
                print(task.project)
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
