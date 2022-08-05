from typing import Union

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .service import *
from .forms import TaskForm, TaskEditForm

def output_all_user_tasks_view(request) -> HttpResponse:
    tasks = get_all_user_tasks(request.user)
    return render(request, '_tasks/tasks.html', {'tasks': tasks})


@login_required(login_url='login')
def create_task_view(request) -> Union[HttpResponseRedirect, HttpResponse]:
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user.profile
            task.save()
        return redirect('all_tasks')    
    return render(request, '_tasks/create.html', {"form": form})


@login_required(login_url='login')
def delete_task_view(request, pk: int) -> HttpResponseRedirect:
    delete_task(pk)
    return redirect("all_tasks")


@login_required(login_url='login')
def update_task_view(request, pk: int) -> Union[HttpResponseRedirect, HttpResponse]:
    task = get_task_by_id(pk)
    form = TaskEditForm(instance=task)
    if request.method == "POST":
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("all_tasks")
    context = {
        'task': task,
        'form': form
        }
    return render(request, '_tasks/update.html', context)


@login_required(login_url='login')
def change_task_status_view(request, pk: int) -> HttpResponseRedirect:
    change_task_status(pk)
    return redirect("all_tasks")
