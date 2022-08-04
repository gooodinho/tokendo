from .service import create_profile, update_user


def create_user_profile_signal(sender, instance, created, **kwargs) -> None:
    if created is True:
        user = instance
        create_profile(user, user.username)


def update_profile_user_signal(sender, instance, created, **kwargs) -> None:
    if created is not True:
        profile = instance
        update_user(profile.user, profile.username, profile.name, profile.email)
