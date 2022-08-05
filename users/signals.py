from .service import create_profile, update_user


def create_user_profile_signal(sender, instance, created, **kwargs) -> None:
    if created is True:
        user = instance
        create_profile(user, user.username, user.email)


def update_profile_user_signal(sender, instance, created, **kwargs) -> None:
    profile = instance
    user = profile.user
    if created == False:
        update_user(user, profile.username, profile.email)

