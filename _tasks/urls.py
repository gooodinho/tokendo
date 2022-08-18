from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.output_inbox_or_project_tasks_view, name="all_tasks"),
    path('create/', views.create_task_view, name="create_task"),
    path('delete/<uuid:pk>/', views.delete_task_view, name="delete_task"),
    path('update/<uuid:pk>/', views.update_task_view, name="update_task"),
    path('change_status/<uuid:pk>/', views.change_task_status_view, name="change_status"),
    path('create-project/', views.create_project_view, name="create_project"),
    path('<uuid:project_id>/', include([
        path('', views.output_inbox_or_project_tasks_view, name="project_tasks"),
        path('create/', views.create_task_view, name="project_create_task"),
        path('delete/<uuid:pk>/', views.delete_task_view, name="project_delete_task"),
        path('update/<uuid:pk>/', views.update_task_view, name="project_update_task"),
        path('change_status/<uuid:pk>/', views.change_task_status_view, name="project_change_status"),
        path('create-project/', views.create_project_view, name="project_create_project"),
    ])),
]
