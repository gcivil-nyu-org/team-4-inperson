from django.shortcuts import render, redirect
from django.http import HttpRequest
from .search_util import *
from courses.course_util import *
from courses.views import course_detail
import logging

logger = logging.getLogger("project")
from util.views import error404


def index(request):
    return render(request, "search/index.html")


def search_by_select(request: HttpRequest):
    search_by = request.GET["search_by"]
    logger.debug(f"search_by: {search_by}")
    if search_by == "CourseID":
        return search_by_course_id(request)
    elif search_by == "CourseName":
        return search_by_course_name(request)
    elif search_by == "ProfessorName":
        return search_by_professor_name(request)


def search_by_course_id(request: HttpRequest) -> render:
    try:
        query = request.GET["query"].strip()
        logger.debug(f"query: {query}")
        course_subject_code, catalog_number = get_sub_code_and_cat_num(query)
        course = course_id_query(course_subject_code, catalog_number)
        return redirect("courses:course_detail", course_id=course.course_id)
    except Exception as e:
        logger.exception(e)
        return render(request, "search/courseId.html", {"query": request.GET["query"].strip()})


def search_by_course_name(request: HttpRequest):
    try:
        query = request.GET["query"].strip()
        logger.debug(f"query: {query}")
        courses = course_query(query)
        filtered_courses = []
        for i in courses:
            current_course_info = get_course_results_info(i)
            if len(current_course_info) > 0:
                filtered_courses.append(current_course_info)
        context = {
            "courses": filtered_courses,
            "query": query,
        }
        return render(request, "search/courseResult.html", context)
    except Exception as e:
        logger.exception(e)
        return error404(request, error = e)


def search_by_professor_name(request):
    try:
        query = request.GET["query"].strip()
        logger.debug(f"query: {query}")
        professors = professor_query(query)
        filtered_professors = []
        for p in professors:
            current_prof_info = get_professor_results_info(p)
            filtered_professors.append(current_prof_info)
        context = {"professors": filtered_professors, "query": query}
        logger.debug(context)
        return render(request, "search/professorResult.html", context)
    except Exception as e:
        logger.exception(e)
        return error404(request, error = e)
