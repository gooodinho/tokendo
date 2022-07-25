from django.shortcuts import render

def test(request):
    return render(request, 'tasks_app/test.html')