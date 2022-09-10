from typing import Union

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .service import *
from .forms import ProfileForm


def user_registration_view(request) -> Union[HttpResponseRedirect, HttpResponse]:
    if request.method == "POST":
        register_new_user_request_handler(request)
        return redirect('all_tasks')
    return render(request, 'users/register.html', {'form': CustomUserCreationForm()})


def user_login_view(request) -> Union[HttpResponse, HttpResponseRedirect]:
    if request.method == "POST":
        username = request.POST['username']
        # Check if user with such credentials exists in database. If true returns User object, if false returns None.
        user = authenticate(request, username=username, password=request.POST['password'])
        if user is not None:
            login(request, user) # Create session in db and in cookies.
            return redirect('inbox')
        else:
            if check_if_user_with_username_exists(username):
                print('Password is incorrect')

    return render(request, "users/login.html")


@login_required(login_url='login')
def user_logout_view(request) -> HttpResponseRedirect:
    logout(request)
    return redirect('inbox')


@login_required(login_url='login')
def user_profile_view(request) -> HttpResponse:
    return render(request, "users/profile.html", {'profile': request.user.profile})


@login_required(login_url='login')
def user_profile_edit_view(request) -> Union[HttpResponse, HttpResponseRedirect]:
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            return redirect('profile')
    context = {'profile': profile, 'form': form}
    return render(request, "users/profile_edit.html", context)
