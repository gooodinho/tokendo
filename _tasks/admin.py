from django.contrib import admin
from django import forms

from .models import Task, Project, SubTask


class TaskAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' not in kwargs:
            try:
                self.fields['project'].queryset = Project.objects.filter(owner=self.instance.owner)
            except:
                pass
        else:
            self.fields['project'].disabled = True


class SubTaskAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' not in kwargs:
            try:
                self.fields['task'].queryset = Task.objects.filter(owner=self.instance.owner)
            except:
                pass
        else:
            self.fields['task'].disabled = True

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('owner', 'created')
        else:
            return ('created',)

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    form = SubTaskAdminForm

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('owner', 'created', 'task')
        else:
            return ('created',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('owner', 'created')
        else:
            return ('created',)
