from django.contrib.auth.models import User
from django.db.models.fields.files import ImageFieldFile

from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm


def register_new_user_handler(request) -> None:
    """Register new user, if data from CustomUserCreationForm is valid."""
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        form.save()       
    else:
        raise Exception


def update_profile_handler(request, profile: Profile) -> None:
    """Update profile, if data from ProfileForm is valid."""
    form = ProfileForm(request.POST, request.FILES, instance=profile)
    if form.is_valid():
        form.save()
    else:
        raise Exception


def check_if_user_with_username_exists(username: str) -> bool:
    try:
        User.objects.get(username=username)
        return True
    except User.DoesNotExist:
        return False


def create_profile(user: User, username: str, email: str, name: str = None) -> Profile:
    profile = Profile.objects.create(
        user=user,
        username=username,
        email=email,
        name=name
    )
    profile.save()
    return profile


def update_user(user: User, username: str, email: str) -> User:
    user.username = username
    user.email = email
    user.save()
    return user


def get_profile_image(id: int) -> ImageFieldFile:
    return Profile.objects.get(id=id).profile_image
