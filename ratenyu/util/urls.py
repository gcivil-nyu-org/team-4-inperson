from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = "util"
urlpatterns = [
    path("", views.error404, name="error404"),
    path("logout", LogoutView.as_view()),
]
