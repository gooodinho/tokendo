from django.db import models
from users.models import Profile

class Task(models.Model):
    task_name = models.CharField('Task name', max_length=1000)
    status = models.BooleanField('Task status', default=False, blank=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name
