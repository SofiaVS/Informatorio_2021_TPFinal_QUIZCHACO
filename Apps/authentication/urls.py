from django.urls import path, include
from . import views


urlpatterns = [
    # authentication
    path('login', views.Login, name='login'),
    path('register', views.Register, name='register'),
    path('logout', views.Logout, name='logout'),
]
