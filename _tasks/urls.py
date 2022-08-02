from django.urls import path 
from . import views


urlpatterns = [
    path('', views.output_all_user_tasks_view, name="all_tasks"),
    path('create/', views.create_task_view, name="create_task"),
    path('delete/<int:pk>/', views.delete_task_view, name="delete_task"),
    path('update/<int:pk>/', views.update_task_view, name="update_task"),
    path('change_status/<int:pk>/', views.change_task_status_view, name="change_status"),
]
