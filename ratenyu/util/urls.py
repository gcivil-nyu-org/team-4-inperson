from django.urls import path

from . import views

app_name = "util"
urlpatterns = [
    path("error", views.error404, name="error404"),
]

