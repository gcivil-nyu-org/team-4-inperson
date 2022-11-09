from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpRequest, Http404

from util.views import error404
from .models import UserDetails
from courses.models import Review
from .forms import UserRegistrationForm
from .user_util import get_user_details

import logging

logger = logging.getLogger("project")


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = update_initial_user(old_username=request.user, form=form)
            user.refresh_from_db()
            user_details = UserDetails(
                name=form.cleaned_data.get("name"),
                user=user,
                major=form.cleaned_data.get("major"),
                student_status=form.cleaned_data.get("student_status"),
            )
            try:
                user_details.save()
            except Exception as e:
                print(e)
            messages.success(
                request, f"Your account has been created. You can log in now!"
            )
            return redirect("users:login")
    else:
        form = UserRegistrationForm(initial={"email": request.user.email})
    context = {"form": form}
    return render(request, "users/register.html", context)


def update_initial_user(old_username: str, form: UserRegistrationForm) -> User:
    user = User.objects.get(username=old_username)
    user.name = form.cleaned_data["name"]
    user.username = form.cleaned_data["username"]
    user.set_password(form.cleaned_data["password1"])
    user.major = form.cleaned_data["major"]
    user.student_status = form.cleaned_data["student_status"]
    user.save()
    return user


def get_profile(request: HttpRequest, user_name: str) -> render:
    if request.user.is_authenticated:
        if request.user.username != user_name:
            return error404(request, "You are not authorized to view this page.")
        context = {}
        user_details = get_user_details(request.user)
        reviews = Review.objects.filter(user=User.objects.get(username=user_name))
        context["user_details"] = user_details
        context["reviews"] = reviews
        logger.debug(f"context : {context}")
    return render(request, "users/profile.html", context)
