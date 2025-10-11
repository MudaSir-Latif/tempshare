from django.urls import path
from core import views as core_views  # ✅ import views from core
from . import views  # this is frontend.views (for home, templates, etc.)


app_name = "frontend"
from core.views import upload_file,submit_url,serve_file,redirect_url
urlpatterns = [
    path("", core_views.home, name="home"),
    path("upload/", core_views.upload_file, name="upload"),
    path("url/", core_views.submit_url, name="submit_url"),
    path("f/<str:token>/", core_views.serve_file, name="serve_file"),
    path("u/<str:token>/", core_views.redirect_url, name="redirect_url"),
]
