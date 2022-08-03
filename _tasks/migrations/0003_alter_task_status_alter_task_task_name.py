# Generated by Django 4.0.6 on 2022-08-03 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_tasks', '0002_alter_task_options_alter_task_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.BooleanField(blank=True, default=False, verbose_name='Task status'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_name',
            field=models.CharField(max_length=1000, verbose_name='Task name'),
        ),
    ]
