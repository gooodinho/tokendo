from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


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
    pass