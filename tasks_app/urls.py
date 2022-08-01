from django.urls import path 
from . import views


urlpatterns = [
    path('', views.output_all_tasks, name="all_tasks"),
    path('create/', views.add_task, name="add_task"),
    path('delete/<int:pk>/', views.delete_task, name="delete_task"),
    path('update/<int:pk>/', views.update_task, name="update_task"),
    path('change_status/<int:pk>/', views.change_task_status, name="change_status"),
]
