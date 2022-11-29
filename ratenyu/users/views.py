from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpRequest
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from util.views import error404
from .models import UserDetails
from courses.models import Review, Course, SavedCourse
from professors.models import Professor
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
            user.student_status = request.POST.get("user_status_input")
            user.save()

        user_details = get_user_details(request.user)
        reviews = Review.objects.filter(user=User.objects.get(username=user_name))

        paginator = Paginator(reviews, 10)
        page_number = request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            "user_details": user_details,
            "reviews": reviews,
            "page_obj": page_obj,
        }
        if request.GET.get("invalid_review_text"):
            context["invalid_review_text"] = True
        logger.debug(f"context : {context}")
        return render(request, "users/profile.html", context)
    else:
        return redirect(reverse("search:index"))


def get_courses(request: HttpRequest, user_name: str):
    mycourses = SavedCourse.objects.filter(user_id=request.user)
    user_details = get_user_details(request.user)
    context = {
        "mycourses": mycourses,
        "user_details": user_details,
    }
    return render(request, "users/my_courses.html", context)


def save_course(request: HttpRequest, user_name: str):
    course = Course.objects.get(pk=request.POST.get("course_id"))
    professor = request.POST.get("save_course_professor_name")
    if (professor):
        professor = Professor.objects.get(name=professor)
        try:
            SavedCourse.objects.create(user_id=request.user, course_id=course, professor_id=professor)
        except:
            return redirect("courses:course_detail", course_id=request.POST.get("course_id"))
    else:
        try:
            SavedCourse.objects.create(course_id=course, user_id=request.user)
        except:
            return redirect("courses:course_detail", course_id=request.POST.get("course_id"))
    return redirect("users:my_courses", user_name=user_name)

def delete_saved_course(request: HttpRequest, course_id: str):
    course = Course.objects.get(pk=course_id)
    user = request.user
    saved_course = SavedCourse.objects.get(user_id = user, course_id = course)
    saved_course.delete()
    return redirect("users:my_courses", user_name=user.username)
