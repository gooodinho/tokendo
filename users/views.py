from typing import Union

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .service import *
from .forms import ProfileForm


def user_registration_view(request) -> Union[HttpResponseRedirect, HttpResponse]:
    if request.method == "POST":
        try:
            register_new_user(request)
            messages.success(request, 'You were successfully registered!')
            return redirect('login')
        except Exception:
            messages.error(request, "Form data are not correct")
    return render(request, 'users/register.html', {'form': CustomUserCreationForm()})


def user_login_view(request) -> Union[HttpResponse, HttpResponseRedirect]:
    if request.method == "POST":
        username = request.POST['username']
        user = authenticate(request, username=username, password=request.POST['password'])  # Check if user with such credentials exists in database. If true returns User object, if false returns None.
        if user is not None:
            login(request, user) # Create session in db and in cookies.
            messages.success(request, 'You were successfully authenticated!')
            return redirect('inbox')
        else:
            if check_if_user_with_username_exists(username):
                messages.warning(request, 'Password is incorrect!')
            else:
                messages.warning(request, 'User with this username does not exist!')

    return render(request, "users/login.html")


@login_required(login_url='login')
def user_logout_view(request) -> HttpResponseRedirect:
    logout(request)
    messages.success(request, 'You were successfully logouted!')
    return redirect('inbox')


@login_required(login_url='login')
def user_profile_view(request) -> HttpResponse:
    return render(request, "users/profile.html", {'profile': request.user.profile})


@login_required(login_url='login')
def user_profile_edit_view(request) -> Union[HttpResponse, HttpResponseRedirect]:
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        try:
            update_profile_handler(request, profile)
            messages.success(request, 'Profile was successfully updated!')
            return redirect('profile')
        except Exception as e:
            messages.warning(request, e)
    context = {'profile': profile, 'form': form}
    return render(request, "users/profile_edit.html", context)
