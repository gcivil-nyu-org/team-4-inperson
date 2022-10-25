from django.db.models import Q
from courses.models import Course, Class, Review
from professors.models import Professor
from courses.course_util import *


def course_query(query: str) -> Class:
    courses = Course.objects.filter(
        Q(course_title__startswith=f"{query} ") |
        Q(course_title__contains=f" {query} ") |
        Q(course_title__endswith=f" {query}") |
        (Q(course_title__startswith=f"{query}") & Q(course_title__endswith=f"{query}"))
    )
    return courses


def professor_query(query: str) -> Class:
    professors = Professor.objects.filter(
        Q(name__startswith=f"{query} ") |
        Q(name__contains=f" {query} ") |
        Q(name__endswith=f" {query}") |
        (Q(name__startswith=f"{query}") & Q(name__endswith=f"{query}"))
    )
    return professors


# this returns a dictionary that contains the
# info necessary to display a course on course results page
def get_course_results_info(course: Class) -> dict:
    classes = Class.objects.filter(course=course.course_id)
    reviews_list = create_review_objects(classes)
    reviews_avg = calculate_rating_avg(reviews_list)
    return {"course_obj": course,
            "reviews_list": reviews_list,
            "reviews_avg": reviews_avg
            }
