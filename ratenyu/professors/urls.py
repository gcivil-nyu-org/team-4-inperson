from django.urls import path

from . import views

app_name = "professors"
urlpatterns = [
    path("<str:professor_id>", views.professor_detail, name="professor_detail"),
    path("<str:review_id>/like", views.like_review, name="like_review"),
    path("<str:review_id>/dislike", views.dislike_review, name="dislike_review"),
]
