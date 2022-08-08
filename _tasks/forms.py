from django.forms import ModelForm

from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['task_name']

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['task_name'].widget.attrs.update({'autofocus': True})
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class TaskEditForm(ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'status']

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['task_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-check-input'})
