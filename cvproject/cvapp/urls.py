from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.LoginView, name="login"),
    path('user_view/', views.UserDataView, name="user_view"),

]
