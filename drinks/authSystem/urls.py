from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.temp_home, name='home'),
    path('login/', views.login_user, name='login_user'),

]