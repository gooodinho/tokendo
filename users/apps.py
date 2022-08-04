from django.apps import AppConfig
from django.db.models.signals import post_save


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = "Users app"

    def ready(self):
        from django.contrib.auth.models import User
        from .models import Profile
        from . import signals

        post_save.connect(
            receiver=signals.create_user_profile_signal, 
            sender=User, 
            dispatch_uid="create_user_profile_signal_id"
            )

        post_save.connect(
            receiver=signals.update_profile_user_signal, 
            sender=Profile, 
            dispatch_uid="update_profile_user_signal_id"
        )
