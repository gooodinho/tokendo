from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.output_inbox_or_project_tasks_view, name="all_tasks"),
    path('task/<uuid:task_id>/', views.task_info_view, name="inbox_task_info"),
    path('create/', views.create_task_view, name="create_task"),
    path('delete/<uuid:pk>/', views.delete_task_view, name="delete_task"),
    path('update/<uuid:pk>/', views.update_task_view, name="update_task"),
    path('change_status/<uuid:pk>/', views.change_task_status_view, name="change_status"),

    path('create-project/', views.create_project_view, name="create_project"),

    path('create-subtask/<uuid:task_id>', views.create_subtask_view, name="create_subtask"),
    path('delete-subtask/<uuid:pk>/', views.delete_subtask_view, name="delete_subtask"),
    path('update-subtask/<uuid:pk>/', views.update_subtask_view, name="update_subtask"),
    path('change_status-subtask/<uuid:pk>/', views.change_subtask_status_view, name="change_subtask_status"),

    path('<uuid:project_id>/', include([
        path('', views.output_inbox_or_project_tasks_view, name="project_tasks"),
        path('task/<uuid:task_id>/', views.task_info_view, name="project_task_info"),
        path('create/', views.create_task_view, name="project_create_task"),
        path('delete/<uuid:pk>/', views.delete_task_view, name="project_delete_task"),
        path('update/<uuid:pk>/', views.update_task_view, name="project_update_task"),
        path('change_status/<uuid:pk>/', views.change_task_status_view, name="project_change_status"),

        path('create-project/', views.create_project_view, name="project_create_project"),

        path('create-subtask/<uuid:task_id>', views.create_subtask_view, name="project_create_subtask"),
        path('delete-subtask/<uuid:pk>/', views.delete_subtask_view, name="project_delete_subtask"),
        path('update-subtask/<uuid:pk>/', views.update_subtask_view, name="project_update_subtask"),
        path('change_status-subtask/<uuid:pk>/', views.change_subtask_status_view, name="project_change_subtask_status"),
    ])),
]
