from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db.models.fields.files import ImageFieldFile

from .models import Profile
from .forms import CustomUserCreationForm


def register_new_user_request_handler(request) -> None:
    """Register new user, if data from CustomUserCreationForm is valid. Login user after registration."""
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        # Create new session
        login(request, user)


def check_user_with_username_exists(username: str) -> bool:
    """Check if user with specific username exists."""
    try:
        User.objects.get(username=username)
        return True
    except User.DoesNotExist:
        print(f'User with username "{username}" does not exist!')
        return False


def check_profile_with_id_exists(id: int) -> bool:
    """Check if Profile with specific id exists."""
    try:
        Profile.objects.get(id=id)
        return True
    except Profile.DoesNotExist:
        return False


def create_profile(user: User, username: str, email: str, name: str = None) -> Profile:
    """Create Profile object for specific user, with username, email and name."""
    profile = Profile.objects.create(
        user=user,
        name=name,
        username=username,
        email=email
    )
    profile.save()
    return profile


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
