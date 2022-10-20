from django.urls import path

from . import views

app_name = 'courses'
urlpatterns = [
    path('<str:course_id>', views.course_detail, name='course_detail'),
]
