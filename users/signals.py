from .service import create_profile, update_user, get_profile_image, check_profile_with_id_exists


def create_user_profile_signal(sender, instance, created, **kwargs) -> None:
    if created is True:
        user = instance
        create_profile(user, user.username, user.email)


def update_profile_user_signal(sender, instance, created, **kwargs) -> None:
    profile = instance
    user = profile.user
    if created == False:
        update_user(user, profile.username, profile.email)


def delete_old_profile_image_signal(sender, instance, **kwargs):
    profile = instance
    if check_profile_with_id_exists(profile.id):
        old_image = get_profile_image(profile.id)
        if 'default' in old_image.url:
            pass
        else:
            new_image = profile.profile_image
            if new_image.url != old_image.url:
                old_image.delete(save=False)
