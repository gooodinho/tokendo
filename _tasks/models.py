from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    task_name = models.CharField('Task name', max_length=1000)
    status = models.BooleanField('Task status', default=False, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name
