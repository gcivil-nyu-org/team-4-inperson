from django.shortcuts import render
from django.http import HttpRequest, Http404
from .models import Course
from .course_util import *


def course_detail(request: HttpRequest, course_id: str):
    try:
        course = Course.objects.get(course_id=course_id)
        classes = Class.objects.filter(course=course)
        professors_list = [cl.professor for cl in classes]
        reviews_list = create_review_objects(classes)
        reviews_avg = calculate_rating_avg(reviews_list)
        context = {
            "classes": classes,
            "course": course,
            "reviews_list": reviews_list,
            "reviews_avg": reviews_avg,
            "professors_list": professors_list,
        }
        return render(request, "courses/detail.html", context)
    except Exception:
        raise Http404("Course does not exist")
