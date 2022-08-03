import uuid

from django.db import models
from django.utils import timezone

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=300, blank=True, null=True)
    username = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(max_length=300, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profiles/", default="profiles/default.png", blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
