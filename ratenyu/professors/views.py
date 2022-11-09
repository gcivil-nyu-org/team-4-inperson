from django.shortcuts import render
from django.http import HttpRequest, Http404
from .models import Professor
from courses.models import Class, Course, Review
from courses.course_util import *
from util.views import error404

def professor_detail(request: HttpRequest, professor_id: str):
    try:
        professor = Professor.objects.get(pk=professor_id)
        classes = Class.objects.filter(professor_id=professor_id)
        courses_list = [cl.course for cl in classes]
        reviews_list = create_review_objects(classes)
        reviews_avg = calculate_rating_avg(reviews_list)
        context = {
            "professor": professor,
            "courses_list": courses_list,
            "reviews_list": reviews_list,
            "reviews_avg": reviews_avg,
        }
        return render(request, "professors/detail.html", context)
    except Exception as e:
        raise error404(request, error = e)
