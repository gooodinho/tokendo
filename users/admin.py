from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        # If profile is already exists - make "user" & "created" fields read-only. 
        # If profile is in process of being created, make only "created" field read-only.
        if obj:
            return ('user', 'created')
        else:
            return ('created',)