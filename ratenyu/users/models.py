from django.db import models
from django.contrib.auth.models import User


class UserDetails(models.Model):
    STATUS_CHOICES = [
        ("Freshman", "Freshman"),
        ("Sophomore", "Sophomore"),
        ("Junior", "Junior"),
        ("Senior", "Senior"),
        ("Master1", "Master1"),
        ("Master2", "Master2"),
        ("PHD", "PHD"),
    ]
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(max_length=100)
    student_status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
    )
