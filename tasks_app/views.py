from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Task


def output_all_tasks(request):
    tasks = []
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        tasks = user.task_set.all()
    context = {'tasks': tasks}
    return render(request, 'tasks_app/tasks.html', context)


@login_required(login_url='login')
def add_task(request):
    if request.method == "POST":
        task_name = request.POST['task_name']
        user = request.user
        Task.objects.create(task_name=task_name, owner=user)
        return redirect('all_tasks')    
    return render(request, 'tasks_app/create.html')


@login_required(login_url='login')
def delete_task(request, pk: int):
    print(pk)
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect("all_tasks")