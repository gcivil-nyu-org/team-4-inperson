from django.db.models import Q
from courses.models import Course, Class, Review
from professors.models import Professor
from courses.course_util import *
import re


def course_query(query: str) -> Class:
    courses = Course.objects.filter(
        Q(course_title__istartswith=f"{query} ")
        | Q(course_title__icontains=f" {query} ")
        | Q(course_title__iendswith=f" {query}")
        | Q(course_title__iexact=query)
    )
    return courses


def professor_query(query: str) -> Class:
    professors = Professor.objects.filter(
        Q(name__istartswith=f"{query} ")
        | Q(name__icontains=f" {query} ")
        | Q(name__iendswith=f" {query}")
        | Q(name__iexact=query)
    )
    return professors


def course_id_query(course_subject_code: str, catalog_number: str) -> Class:
    course = Course.objects.get(
        course_subject_code=course_subject_code.upper(),
        catalog_number=catalog_number.upper(),
    )
    return course


# this returns a dictionary that contains the
# info necessary to display a course on course results page


def get_course_results_info(course: Class) -> dict:
    classes = Class.objects.filter(course=course.course_id)
    if len(classes) == 0:
        return {}
    reviews_list = create_review_objects(classes)
    reviews_avg = calculate_rating_avg(reviews_list)
    return {
        "course_obj": course,
        "reviews_list": reviews_list,
        "reviews_avg": reviews_avg,
        "last_offered": max([cl.last_offered for cl in classes])
    }


def get_professor_results_info(professor: Class) -> dict:
    classes = Class.objects.filter(professor=professor.professor_id)
    reviews_list = create_review_objects(classes)
    reviews_avg = calculate_rating_avg(reviews_list)
    return {
        "professor_obj": professor,
        "reviews_list": reviews_list,
        "reviews_avg": reviews_avg,
    }


def get_sub_code_and_cat_num(query: str) -> tuple:
    course_subject_code = re.search(r"^[a-zA-Z]+[-\s][a-zA-Z]{2}", query).group(0)
    if "-" not in course_subject_code:
        course_subject_code = course_subject_code.replace(" ", "-")
    catalog_number = re.search(r"[0-9]{4}", query).group(0)
    return course_subject_code, catalog_number
