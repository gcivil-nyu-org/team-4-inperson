from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    STATUS_CHOICES = [
        ("", "-- Grade Level --"),
        ("freshman", "Freshman"),
        ("sophomore", "Sophomore"),
        ("junior", "Junior"),
        ("senior", "Senior"),
        ("master1", "Master1"),
        ("master2", "Master2"),
        ("phd", "PHD"),
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
        widget=forms.TextInput(
            attrs={"class": "register-input", "placeholder": "Major"}
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
            attrs={"class": "register-input", "placeholder": "NYU Email"}
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

    def student_status_selected(self) -> bool:
        return self.fields["student_status"] != ""
