from django.shortcuts import render
from django.http import HttpRequest, Http404
from django.db.models import Q
from courses.models import Course, Class, Review
from professors.models import Professor
from .search_util import *
from courses.course_util import *


def index(request):
    return render(request, "search/index.html")


def search_by_select(request: HttpRequest):
    search_by = request.GET["search_by"]
    if search_by == "CourseID":
        return search_by_course_id(request)
    elif search_by == "CourseName":
        return search_by_course_name(request)
    elif search_by == "ProfessorName":
        return search_by_professor_name(request)


def search_by_course_id(request: HttpRequest):
    return render(request, "search/courseResult.html")


def search_by_course_name(request: HttpRequest):
    try:
        query = request.GET["query"].strip()
        print(query)
        courses = course_query(query)
        filtered_courses = []
        for i in courses:
            current_course_info = get_course_results_info(i)
            filtered_courses.append(current_course_info)
        context = {
            "courses": filtered_courses,
            "query": query,
        }
        return render(request, "search/courseResult.html", context)
    except:
        raise Http404("Something went wrong")


def search_by_professor_name(request):
    try:
        query = request.GET["query"]
        professors = Professor.objects.filter(
            Q(name__startswith=f"{query} ")
            | Q(name__contains=f" {query} ")
            | Q(name__endswith=f" {query}")
        )
        context = {"professors": professors}
        return render(request, "search/professorResult.html", context)
    except:
        raise Http404("Something went wrong")
