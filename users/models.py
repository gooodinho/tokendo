import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=300, blank=True, null=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(max_length=300, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profiles/", default="/profiles/default.png")
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username
