from tkinter.messagebox import NO
from typing import Union

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

from .models import Profile


def register_new_user_request_handler(request) -> None:
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = register_new_user(form)
        # Create new session
        login(request, user)

def register_new_user(form: UserCreationForm) -> User:
    user = form.save(commit=False)
    user.save()
    return user


def check_user_with_username_exists(username: str) -> bool:
    try:
        User.objects.get(username=username)
        return True
    except Exception as e:
        print(f'User with username "{username}" does not exist!')
        return False


def create_profile(user: User, username: str, name: str = None, email: str = None) -> Profile:
    profile = Profile.objects.create(
        user=user,
        name=name,
        username=username,
        email=email
    )
    profile.save()
    return profile


def update_profile(profile: Profile, username: str, name: str, email: str, profile_image) -> Profile:
    profile.username = username
    profile.name = name
    profile.email = email
    profile.profile_image = profile_image
    profile.save()
    return profile

def update_user(user: User, username: str, name: str, email: str) -> User:
    user.username = username
    user.first_name = name
    user.email = email
    user.save()
    return user
