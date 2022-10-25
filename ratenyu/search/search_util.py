from django.db.models import Q
from courses.models import Course, Class, Review
from professors.models import Professor
from courses.course_util import *


def course_query(query: str) -> Class:
    courses = Course.objects.filter(
        Q(course_title__istartswith=f"{query} ") |
        Q(course_title__icontains=f" {query} ") |
        Q(course_title__iendswith=f" {query}") |
        Q(course_title__iexact=query)
    )
    return courses


def professor_query(query: str) -> Class:
    professors = Professor.objects.filter(
        Q(name__istartswith=f"{query} ") |
        Q(name__icontains=f" {query} ") |
        Q(name__iendswith=f" {query}") |
        Q(name__iexact=query)
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
