# core/urls.py
from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("upload/", views.upload_file, name="upload"),
    path("url/", views.submit_url, name="submit_url"),
    path("f/<str:token>/", views.serve_file, name="serve_file"),
    path("u/<str:token>/", views.redirect_url, name="redirect_url"),
]
