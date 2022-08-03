from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login_view, name="login"),
    path('register/', views.user_registration_view, name="register"),
    path('logout/', views.user_logout_view, name="logout"),
    path('profile/', views.user_profile_view, name="profile"),
]