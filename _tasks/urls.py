from django.urls import path
from . import views


urlpatterns = [
    path('', views.output_inbox_tasks_view, name="inbox"),
    path('<uuid:project_id>/', views.output_project_tasks_view, name='project_tasks'),
    path('change_status/<uuid:task_id>/', views.change_task_status_view, name='change_status'),
    path('create/', views.create_task_view, name='create_task'),
    path('delete/<uuid:task_id>/', views.delete_task_view, name='delete_task'),
    path('update/<uuid:task_id>/', views.update_task_view, name="update_task"),
    path('task/<uuid:task_id>/', views.task_info_view, name='task_info'),
    path('task/<uuid:task_id>/<uuid:project_id>', views.task_info_view, name='task_info'),
    path('create_project/', views.create_project_view, name="create_project"),
    path('change_status_subtask/<uuid:subtask_id>/', views.change_subtask_status_view, name='change_subtask_status'),
    path('create_subtask/<uuid:task_id>/', views.create_subtask_view, name='create_subtask'),
    path('delete_subtask/<uuid:subtask_id>/', views.delete_subtask_view, name='delete_subtask'),
    path('update_subtask/<uuid:subtask_id>/', views.update_subtask_view, name='update_subtask'),
]
