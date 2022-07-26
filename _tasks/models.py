import uuid

from django.db import models
from django.utils import timezone

from users.models import Profile


class Project(models.Model):
    title = models.CharField('Project title', max_length=300)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Task(models.Model):
    task_name = models.CharField('Task name', max_length=1000)
    status = models.BooleanField('Task status', default=False, blank=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.task_name

    class Meta:
        ordering = ['status']



class SubTask(models.Model):
    task_name = models.CharField('Subtask name', max_length=1000)
    status = models.BooleanField('Subtask status', default=False, blank=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.task_name

    class Meta:
        ordering = ['status']