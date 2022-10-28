
from telnetlib import STATUS
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    STATUS_CHOICES = [
        ("freshman", "Freshman"),
        ("sophomore", "Sophomore"),
        ("junior", "Junior"),
        ("senior", "Senior"),
        ("master1", "Master1"),
        ("master2", "Master2"),
        ("phd", "PHD")
    ]
    name = forms.CharField(max_length=100)
    major = forms.CharField(max_length=100)
    student_status = forms.CharField(
        label='Student Status', widget=forms.Select(choices=STATUS_CHOICES))

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password1',
                  'password2', 'major', 'student_status']
