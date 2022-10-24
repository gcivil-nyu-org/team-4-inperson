from django.urls import path

from . import views

app_name = "professors"
urlpatterns = [
    path("<str:professor_id>", views.professor_detail, name="professor_detail"),
]
