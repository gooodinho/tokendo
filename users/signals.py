from .service import create_profile, update_profile


def create_user_profile_signal(sender, instance, created, **kwargs):
    if created is True:
        user = instance
        create_profile(user, user.username)


def update_user_profile_signal(sender, instance, created, **kwargs):
    if created is not True:
        user = instance
        update_profile(user, user.username, user.first_name, user.email)
