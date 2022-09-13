from .models import Profile
from .service import create_profile, update_user, get_profile_image

def create_user_profile_signal(sender, instance, created, **kwargs) -> None:
    """Signal for automatic Profile object creation for User, after registration."""
    if created is True:
        user = instance
        create_profile(user, user.username, user.email)


def update_profile_user_signal(sender, instance, created, **kwargs) -> None:
    """Signal for auto update User when User's Profile is updated."""
    if created == False:
        profile = instance
        user = profile.user
        update_user(user, profile.username, profile.email)


def delete_old_profile_image_signal(sender, instance, **kwargs) -> None:
    """Signal to delete old profile_image file, before updating and saving a new one."""
    profile = instance
    try:
        old_image = get_profile_image(profile.id)
        if 'default' in old_image.url:
            pass
        else:
            new_image = profile.profile_image
            if new_image.url != old_image.url:
                old_image.delete(save=False)
    except Profile.DoesNotExist:
        pass
