from .service import create_profile, update_user, get_profile_image, check_profile_with_id_exists
from _tasks.service import create_inbox_project


def create_user_profile_signal(sender, instance, created, **kwargs) -> None:
    """Signal for automatic Profile object creation for User, after registration."""
    if created is True:
        user = instance
        profile = create_profile(user, user.username, user.email)
        create_inbox_project(profile)


def update_profile_user_signal(sender, instance, created, **kwargs) -> None:
    """Signal for auto update User when User's Profile is updated."""
    profile = instance
    user = profile.user
    if created == False:
        update_user(user, profile.username, profile.email)


def delete_old_profile_image_signal(sender, instance, **kwargs) -> None:
    """Signal to delete old profile_image file, before updating and saving a new one."""
    profile = instance
    if check_profile_with_id_exists(profile.id):
        old_image = get_profile_image(profile.id)
        if 'default' in old_image.url:
            pass
        else:
            new_image = profile.profile_image
            if new_image.url != old_image.url:
                old_image.delete(save=False)
