import logging
from json import dumps
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from courses.models import Review
from professors.models import Professor
from .course_util import *
from util.views import error404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

LOGGER = logging.getLogger("project")


def course_detail(request: HttpRequest, course_id: str):
    LOGGER.debug(f"course_detail: {course_id}")
    try:
        if request.method == "GET":
            return load_course_detail(request, course_id)
        elif request.method == "POST" and "submit" in request.POST:
            LOGGER.debug(request.POST)
            review, message = add_review_from_details(request)
            return load_course_detail(request, course_id, review, message)
        else:
            LOGGER.error(request.POST)
            return error404(request, error="Invalid request")
    except Exception as e:
        return error404(request, error=e)


def load_course_detail(request: HttpRequest, course_id: str, review: bool = None,
                       review_message: str = "") -> HttpResponse:
    try:
        course = Course.objects.get(course_id=course_id)
        classes = Class.objects.filter(course=course)
        professors_list = [cl.professor for cl in classes]
        reviews_list = create_review_objects(classes)
        reviews_avg = calculate_rating_avg(reviews_list)

        paginator = Paginator(reviews_list, 10)
        page_number = request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        if review is not None:
            context = {
                "classes": classes,
                "course": course,
                "reviews_list": reviews_list,
                "reviews_avg": reviews_avg,
                "professors_list": professors_list,
                "review_saved": review,
                "review_message": review_message,
                "page_obj": page_obj,
            }
        else:
            context = {
                "classes": classes,
                "course": course,
                "reviews_list": reviews_list,
                "reviews_avg": reviews_avg,
                "professors_list": professors_list,
                "page_obj": page_obj,
            }
        LOGGER.debug(context)
        return render(request, "courses/detail.html", context)
    except Exception as e:
        return error404(request, error=e)


def add_review(request):
    all_courses = Course.objects.only(
        "course_subject_code", "catalog_number", "course_title"
    )
    all_courses_list = [
        {
            "course_title": course.course_title.replace("'", ""),
            "course_id": f"{course.course_subject_code} {course.catalog_number}",
        }
        for course in all_courses
    ]
    all_course_ids = [
        f"{course.course_subject_code} {course.catalog_number}"
        for course in all_courses
    ]
    all_professors = Professor.objects.only("professor_id", "name")
    context = {
        "courses": all_courses,
        "professors": all_professors,
        "course_ids": all_course_ids,
        "courses_json": dumps(all_courses_list),
    }
    if request.method == "GET":
        if request.user.id is None:
            return redirect(reverse("search:index"))
        return render(request, "courses/add_review.html", context)
    elif request.method == "POST":
        user = User.objects.get(username=request.user)
        try:
            if not text_is_valid(request.POST["review_text"]):
                context["review_text_invalid"] = True
                return render(request, "courses/add_review.html", context)

            new_review = save_new_review(
                user=user,
                user_entered_course_id=request.POST["add_review_course_id"],
                professor_name=request.POST["add_review_professor_name"],
                review_rating=request.POST["review_rating"],
                review_text=request.POST["review_text"],
            )
            LOGGER.info(f"Created new Review: {new_review}")
            context["review_saved"] = True
            return render(request, "courses/add_review.html", context)
        except Exception as e:
            LOGGER.exception(f"Could not create review, encountered error: {e}")
            context["review_saved"] = False
            return render(request, "courses/add_review.html", context)


def delete_review(request, review_id: str):
    try:
        r = Review.objects.get(pk=review_id)
        r.delete()
        add_redirect_message(request=request, message="Your review was deleted.", success=True)
        return redirect('users:profile', user_name=request.user)
    except Exception as e:
        return error404(request, error=e)
