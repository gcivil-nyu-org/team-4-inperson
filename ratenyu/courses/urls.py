from django.urls import path

from . import views

app_name = "courses"
urlpatterns = [
    path("add_review/", views.add_review, name="add_review"),
    path("add_review", views.add_review, name="add_review"),
    path("<str:review_id>/delete", views.delete_review, name="delete_review"),
    path("edit_review", views.edit_review, name="edit_review"),
    path("<str:review_id>/delete", views.delete_review, name="delete_review"),
    path("<str:course_id>", views.course_detail, name="course_detail"),
]
