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
    name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'input-box', 'placeholder': 'Enter your name'}), label="Name")
    major = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'class': 'input-box', 'placeholder': 'Enter your major'}), label="Major")
    student_status = forms.CharField(
        label='Student Status', widget=forms.Select(attrs={'class': 'input-box'}, choices=STATUS_CHOICES))
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'input-box', 'placeholder': 'This appears on your profile'}), label="Username")
    email = forms.CharField(
        max_length=100, widget=forms.EmailInput(attrs={'class': 'input-box', 'placeholder': 'Enter your NYU email'}), label="Email")
    password1 = forms.CharField(
        max_length=100, widget=forms.PasswordInput(attrs={'class': 'input-box', 'placeholder': 'Enter password'}), label="Create Password")
    password2 = forms.CharField(
        max_length=100, widget=forms.PasswordInput(attrs={'class': 'input-box', 'placeholder': 'Re-Enter password'}), label="Retype Password")

    class Meta:
        model = User
        fields = ['name', 'email', 'username',
                  'password1', 'password2', 'major', 'student_status']
