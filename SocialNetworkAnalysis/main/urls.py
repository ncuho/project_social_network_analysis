from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("login", views.login_views, name="login"),
    path('register', views.regist_views, name='register'),
    path("getlinks", views.get_links_view, name="getlinks")
]
