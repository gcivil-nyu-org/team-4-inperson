from json import dumps
from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404
from django.urls import reverse
from .models import Course, Review
from professors.models import Professor
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
            "reviews_list": reviews_list
        }
        return render(request, "courses/detail.html", context)
    except Exception:
        raise Http404("Course does not exist")


def add_review(request):
    # Assuming we'll need all courses and professors in the context for auto-fill
    all_courses = Course.objects.only("course_subject_code", "catalog_number", "course_title")
    all_courses_list = [{
        "course_title": course.course_title.replace("'", ""),
        "course_id": f"{course.course_subject_code} {course.catalog_number}"
    } for course in all_courses]
    all_course_ids = [f"{course.course_subject_code} {course.catalog_number}" for course in all_courses]
    all_professors = Professor.objects.only("professor_id", "name")
    context = {
        "courses": all_courses,
        "professors": all_professors,
        "course_ids": all_course_ids,
        "courses_json": dumps(all_courses_list)
    }
    if request.method == "GET":
        if request.user.id is None:
            return redirect(reverse('search:index'))
        return render(request, 'courses/add_review.html', context)
    elif request.method == "POST":
        try:
            save_new_review(
                user=request.user,
                user_entered_course_id=request.POST["course_id"],
                professor_name=request.POST["professor_name"],
                review_rating=request.POST["review_rating"],
                review_text=request.POST["review_text"],
            )
        except:
            context["review_saved"] = False
            return render(request, 'courses/add_review.html', context)
        context["review_saved"] = True
        return render(request, 'courses/add_review.html', context)
