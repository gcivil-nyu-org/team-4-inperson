from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Professor
from courses.models import Class, Course, Review
from courses.course_util import *
from util.views import error404
import logging

LOGGER = logging.getLogger("project")


def professor_detail(request: HttpRequest, professor_id: str):
    LOGGER.debug(f"professor_detail: {professor_id}")
    try:
        if request.method == "GET":
            return load_professor_detail(request, professor_id)
        elif request.method == "POST" and "submit" in request.POST:
            LOGGER.debug(request.POST)
            review, message = add_review_from_details(request)
            return load_professor_detail(request, professor_id, review, message)
        else:
            LOGGER.error(request.POST)
            return error404(request, error = "Invalid request")
    except Exception as e:
        LOGGER.exception(e)
        return error404(request, error = e)


def load_professor_detail(request: HttpRequest, professor_id: str, review: bool = None, review_message: str = "")-> HttpResponse:
    try:
        professor = Professor.objects.get(pk=professor_id)
        classes = Class.objects.filter(professor_id=professor_id)
        courses_list = [cl.course for cl in classes]
        reviews_list = create_review_objects(classes)
        reviews_avg = calculate_rating_avg(reviews_list)
        if review is not None:
            context = {"professor": professor, "courses_list": courses_list, "reviews_list": reviews_list,"reviews_avg": reviews_avg, "review_saved": review, "review_message" : review_message}
        else :
            context = {"professor": professor, "courses_list": courses_list, "reviews_list": reviews_list,"reviews_avg": reviews_avg}
        return render(request, "professors/detail.html", context)
    except Exception as e:
        return error404(request, error = e)