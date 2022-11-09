from django.urls import path

from . import views

app_name = "courses"
urlpatterns = [
    path("add_review/", views.add_review, name="add_review"),
    path("add_review", views.add_review, name="add_review"),
    path("<str:course_id>", views.course_detail, name="course_detail"),
]
