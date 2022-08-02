from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login



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
