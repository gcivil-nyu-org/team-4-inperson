from django.urls import path

from . import views

app_name = "util"
urlpatterns = [
    path("", views.error404, name="error404"),
]

#404 url handler
handler404 = "util.views.page_not_found"
