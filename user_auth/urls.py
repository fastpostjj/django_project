from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from user_auth.apps import UserAuthConfig
from user_auth.views import ProfileUpdateView, RegisterView


app_name = UserAuthConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='user_auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),

    ]