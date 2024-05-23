from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("login", views.login_views, name="login"),
    path('register', views.regist_views, name='register'),
    path("getlinks", views.get_links_view, name="getlinks"),
    path("addlinks", views.add_links_by_user, name="addlinks"),
    path("addinfo", views.add_info_by_links, name="addinfo"),
    path("getfrendinfo", views.get_frends_by_link_for_bd, name="getfrendinfo"),
    path("gigachatconnectinfo", views.giga_chat_ai_connect_info, name="gigachatconnectinfo"),
    path("gigachatgetinfo", views.giga_chat_ai_get_info, name="gigachatgetinfo"),
    path("gigachat", views.giga_chat_ai, name="gigachat")
]