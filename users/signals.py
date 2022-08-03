from .service import create_profile, get_profile_by_user, update_profile


def create_user_profile_signal(sender, instance, created, **kwargs) -> None:
    if created is True:
        user = instance
        create_profile(user, user.username)


def update_user_profile_signal(sender, instance, created, **kwargs) -> None:
    if created is not True:
        user = instance
        if get_profile_by_user(user) is not None:
            update_profile(user, user.username, user.first_name, user.email)
        else:
            create_profile(user, user.username)
