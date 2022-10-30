from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages

from .models import UserDetails
from .forms import UserRegistrationForm


def home(request):
    return render(request, 'users/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user_details = UserDetails(
                name=form.cleaned_data.get('name'),
                user=user,
                major=form.cleaned_data.get('major'),
                student_status=form.cleaned_data.get('student_status'),
            )
            try:
                user_details.save()
            except Exception as e:
                print(e)
            messages.success(
                request, f'Your account has been created. You can log in now!')
            return redirect('users:login')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)
