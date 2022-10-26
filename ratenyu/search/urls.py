from django.urls import path

from . import views

app_name = "search"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search_by_select, name="search_by_select"),
]
