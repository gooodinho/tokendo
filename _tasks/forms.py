from django.forms import ModelForm

from .models import Task, Project, SubTask

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['task_name']

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['task_name'].widget.attrs.update({'autofocus': True})
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class SubTaskForm(ModelForm):
    class Meta:
        model = SubTask
        fields = ['task_name']

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['task_name'].widget.attrs.update({'autofocus': True})
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class TaskEditForm(ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'status', 'project']


    def __init__(self, profile, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['task_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['project'].queryset = Project.objects.filter(owner=profile)
        self.fields['project'].empty_label = "Inbox"


class SubTaskEditForm(ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'status']

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['task_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-check-input'})


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title']
