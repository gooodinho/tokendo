from typing import Union

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .crud import *


def output_all_user_tasks_view(request) -> HttpResponse:
    tasks = get_all_user_tasks(request.user)
    return render(request, '_tasks/tasks.html', {'tasks': tasks})


@login_required(login_url='login')
def create_task_view(request) -> Union[HttpResponseRedirect, HttpResponse]:
    if request.method == "POST":
        create_task(request.POST['task_name'], request.user)
        return redirect('all_tasks')    
    return render(request, '_tasks/create.html')


@login_required(login_url='login')
def delete_task_view(request, pk: int) -> HttpResponseRedirect:
    delete_task(pk)
    return redirect("all_tasks")


@login_required(login_url='login')
def update_task_view(request, pk: int) -> Union[HttpResponseRedirect, HttpResponse]:
    if request.method == "POST":
        update_task(pk, 
                    request.POST["task_name"], 
                    True if "on" in request.POST["status"] else False)
        return redirect("all_tasks")
    return render(request, '_tasks/update.html', {'task': get_task_by_id(id)})


@login_required(login_url='login')
def change_task_status_view(request, pk: int) -> HttpResponseRedirect:
    change_task_status(pk)
    return redirect("all_tasks")
