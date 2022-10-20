import re
from django.http import HttpRequest, Http404
from django.shortcuts import render
from django.http import HttpRequest, Http404
from django.db.models import Q
from courses.models import Course, Class, Review
from professors.models import Professor
from .search_util import *
from courses.course_util import *
from courses.views import course_detail


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


'''
This function is used in the search page.
A user can search course by id, professor name, or course name.
This function will redirect the search result to the corresponding page.
'''


def search_by_id_func(request: HttpRequest):
    try:
        search_by = request.GET['search_by']
        query = request.GET['query']
        print(search_by)
        print(query)
        if search_by == 'CourseID':
            try:
                course_subject_code = re.search(
                    r'^[a-zA-Z]{4}|^[a-zA-Z]{2}[-\s][a-zA-Z]{2}', query).group(0)
                if len(course_subject_code) == 4:
                    course_subject_code = course_subject_code[:2] + \
                        '-' + course_subject_code[2:]
                elif len(course_subject_code) == 5 and course_subject_code[2] == ' ':
                    course_subject_code = course_subject_code[:2] + \
                        '-' + course_subject_code[2:]
                catalog_number = re.search(r'[0-9]{4}', query).group(0)
                course_id = Course.objects.get(
                    course_subject_code=course_subject_code, catalog_number=catalog_number)
                return course_detail(request, course_id.course_id)
            except:
                raise Http404("Invalid Course ID")
        return render(request, "search/courseResult.html")
    except:
        raise Http404("Something went wrong")


'''
This function is used in the search page.
A user can search course by id, professor name, or course name.
This function will redirect the search result to the corresponding page.
'''


def search_by_id_func(request: HttpRequest):
    try:
        search_by = request.GET['search_by']
        query = request.GET['query']
        print(search_by)
        print(query)
        if search_by == 'CourseID':
            try:
                course_subject_code = re.search(
                    r'^[a-zA-Z]{4}|^[a-zA-Z]{2}[-\s][a-zA-Z]{2}', query).group(0)
                if len(course_subject_code) == 4:
                    course_subject_code = course_subject_code[:2] + \
                        '-' + course_subject_code[2:]
                elif len(course_subject_code) == 5 and course_subject_code[2] == ' ':
                    course_subject_code = course_subject_code[:2] + \
                        '-' + course_subject_code[2:]
                catalog_number = re.search(r'[0-9]{4}', query).group(0)
                course_id = Course.objects.get(
                    course_subject_code=course_subject_code, catalog_number=catalog_number)
                return course_detail(request, course_id.course_id)
            except:
                raise Http404("Invalid Course ID")
        return render(request, "search/courseResult.html")
    except:
        raise Http404("Something went wrong")
