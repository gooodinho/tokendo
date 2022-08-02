from typing import Union

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm

from .service import *


def user_registration_view(request) -> Union[HttpResponseRedirect, HttpResponse]:
    if request.method == "POST":
        register_new_user_request_handler(request)
        return redirect('all_tasks')
    return render(request, 'users/register.html', {'form': UserCreationForm()})


def user_login_view(request) -> Union[HttpResponse, HttpResponseRedirect]:
    if request.method == "POST":
        username = request.POST['username']
        if check_user_with_username_exists(username):
            # Check if user with such credentials exists in database. If true returns User object, if false returns None.
            user = authenticate(request, username=username, password=request.POST['password'])
            if user is not None:
                login(request, user) # Create session in db and in cookies.
                return redirect('all_tasks')
            else:
                print('Password is incorrect')
    return render(request, "users/login.html")


def user_logout_view(request) -> HttpResponseRedirect:
    logout(request)
    return redirect('all_tasks')
