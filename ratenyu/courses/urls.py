from django.urls import path

from . import views

app_name = 'courses'
urlpatterns = [
    path('<str:class_id>', views.class_detail, name='class_detail'),
]
