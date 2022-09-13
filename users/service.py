from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db.models.fields.files import ImageFieldFile

from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm


def register_new_user(request) -> None:
    """Register new user, if data from CustomUserCreationForm is valid."""
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        form.save()       
    else:
        raise Exception


def update_profile_handler(request, profile) -> None:
    form = ProfileForm(request.POST, request.FILES, instance=profile)
    if form.is_valid():
        profile = form.save()
    else:
        raise Exception("Form data are not correct!")


def check_if_user_with_username_exists(username: str) -> bool:
    """Check if user with specific username exists."""
    try:
        User.objects.get(username=username)
        return True
    except User.DoesNotExist:
        print(f'User with username "{username}" does not exist!')
        return False


def create_profile(user: User, username: str, email: str, name: str = None) -> Profile:
    """Create Profile object for specific user, with username, email and name."""
    profile = Profile.objects.create(
        user=user,
        username=username,
        email=email,
        name=name
    )
    profile.save()
    return profile

# Проверить используеться ли где-то
def update_profile(profile: Profile, username: str, name: str, email: str, profile_image) -> Profile:
    """Update existing Profile object, with new username, name, email and profile_image."""
    profile.username = username
    profile.name = name
    profile.email = email
    profile.profile_image = profile_image
    profile.save()
    return profile

def update_user(user: User, username: str, email: str) -> User:
    """Update existing User object, with new username and email."""
    user.username = username
    user.email = email
    user.save()
    return user

def get_profile_image(id: int) -> ImageFieldFile:
    """Found specific Profile by id and return it's profile_image file."""
    return Profile.objects.get(id=id).profile_image
