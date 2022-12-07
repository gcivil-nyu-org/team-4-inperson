from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserDetails

class UserRegistrationForm(UserCreationForm):

    STATUS_CHOICES = [
        ("", "-- Grade Level --"),
        ("Freshman", "Freshman"),
        ("Sophomore", "Sophomore"),
        ("Junior", "Junior"),
        ("Senior", "Senior"),
        ("Master1", "Master1"),
        ("Master2", "Master2"),
        ("Phd", "PHD"),
    ]
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "register-input", "placeholder": "Name"}
        ),
        label="Name",
    )
    major = forms.CharField(
        max_length=100,
        widget=forms.Select(
            attrs={"class": "dropdown-register"}, choices=UserDetails.LIST_OF_MAJORS
        ),
        label="Major",
    )
    student_status = forms.CharField(
        label="Student Status",
        widget=forms.Select(
            attrs={"class": "dropdown-register"}, choices=STATUS_CHOICES
        ),
    )
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "register-input", "placeholder": "Username"}
        ),
        label="Username",
    )
    email = forms.CharField(
        max_length=100,
        widget=forms.EmailInput(
            attrs={"class": "register-input", "placeholder": "NYU Email", "readonly":"True"}
        ),
        label="Email",
    )
    password1 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class": "register-input", "placeholder": "Password"}
        ),
        label="Create Password",
    )
    password2 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class": "register-input", "placeholder": "Re-Enter Password"}
        ),
        label="Retype Password",
    )

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "username",
            "password1",
            "password2",
            "major",
            "student_status",
        ]
