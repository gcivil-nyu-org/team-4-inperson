from django.urls import path

from . import views

app_name = "search"
urlpatterns = [
    path("", views.index, name="index"),
    path(
        "<str:professor_name>/professor_result",views.professor_result,name="professor_result"),
    path("<str:course_name>/course_result", views.course_result, name="course_result"),
    path("search_by_select", views.search_by_select, name="search_by_select")
]
