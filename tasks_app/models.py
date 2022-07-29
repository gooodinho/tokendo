from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    task_name = models.CharField('task\'s name', max_length=1000)
    status = models.BooleanField('task\'s status(done?)', default=False, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "task"

    def __str__(self):
        return self.task_name
