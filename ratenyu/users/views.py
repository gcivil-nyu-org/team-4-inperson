from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpRequest
from django.urls import reverse

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
            storage = messages.get_messages(request)
            storage.used = True       
            messages.success(
                request, "Your account has been created. You can log in now!"
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
    '''
    This function loads details of the user and the reviews that the user has written.
    The function only loads the details of the user if the user is logged in and for that user only.
    It will redirect to index page if the user is not logged in.
    it will redirect to error page if the user is logged in but is trying to view details of another user.
    '''
    if request.user.is_authenticated:
        if request.user.username != user_name:
            return error404(request, "You are not authorized to view this page.")

        if request.method == "POST":
            user = get_user_details(request.user)
            user.name = request.POST.get("user_name_input")
            user.major = request.POST.get("user_major_input")
            # request.user.username = request.POST.get("user_username_input")
            user.student_status = request.POST.get("user_status_input")
            user.save()

        user_details = get_user_details(request.user)
        reviews = Review.objects.filter(user=User.objects.get(username=user_name))
        context = {
            "user_details": user_details,
            "reviews": reviews
        }
        if request.GET.get("invalid_review_text"):
            context["invalid_review_text"] = True
        logger.debug(f"context : {context}")
        return render(request, "users/profile.html", context)
    else:
        return redirect(reverse("search:index"))
