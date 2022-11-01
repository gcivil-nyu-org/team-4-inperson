from django.db import models
from django.contrib.auth.models import User


class UserDetails(models.Model):
    STATUS_CHOICES = [
        ("freshman", "Freshman"),
        ("sophomore", "Sophomore"),
        ("junior", "Junior"),
        ("senior", "Senior"),
        ("master1", "Master1"),
        ("master2", "Master2"),
        ("phd", "PHD"),
    ]
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(max_length=100)
    student_status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
    )
