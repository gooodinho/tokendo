from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def user_register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save new user
            user = form.save(commit=False)
            user.save()
            print('User successfully registered!')
            # Create new session
            login(request, user)
            return redirect('all_tasks')
    context = {'form': form}
    return render(request, 'users/register.html', context=context)


def user_login(request):
    if request.method == "POST":
        
        username = request.POST['username']
        password = request.POST['password']

        # Check if user with this username exists
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print(e)
            print(f'User with username "{username}" does not exist!')

        # Check if user with such credentials exists in database. If true returns User object, if false returns None.
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Create session in db and in cookies.
            login(request, user)
            return redirect('all_tasks')
        else:
            print('Username or password is incorrect')

    return render(request, "users/login.html")
