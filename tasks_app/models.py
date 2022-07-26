from django.db import models

class Task(models.Model):
    task_name = models.CharField('task\'s name', max_length=1000)

    class Meta:
        verbose_name = "task"

    def __str__(self):
        return self.task_name
