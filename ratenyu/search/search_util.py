from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import HttpRequest
from courses.models import Course, Class
from professors.models import Professor
from courses.course_util import *
from fuzzywuzzy import fuzz

# Similarity Thresholds above which course results must be displayed
COURSE_WRATIO = 90
COURSE_SORT_RATIO = 50
COURSE_PARTIAL_RATIO = 70

# Similarity Thresholds above which professor results must be displayed
PROFESSOR_RATIO = 70

# Uses (descending) fuzzy ratio as a treshold to list out courses closest to the query
def course_query(query: str) -> QuerySet[Course]:
    if (len(query) > 3):
        courses = {}
        sorted_course = []
        all_courses = Course.objects.all()
        for i in all_courses:
            if (fuzz.WRatio(query, i.course_title) >= COURSE_WRATIO or fuzz.token_sort_ratio(query, i.course_title) >= COURSE_SORT_RATIO or fuzz.partial_ratio(query, i.course_title) >= COURSE_PARTIAL_RATIO):
                courses[i] = fuzz.WRatio(query, i.course_title)
        sorted_course = sorted(courses, key=courses.get, reverse=True)
        return sorted_course
    else:
        courses = Course.objects.filter(
        Q(course_title__istartswith=f"{query} ")
        | Q(course_title__icontains=f" {query} ")
        | Q(course_title__iendswith=f" {query}")
        | Q(course_title__iexact=query)
        )
        return courses

# Uses (descending) fuzzy ratio as a treshold to list out professors closest to the query
def professor_query(query: str) -> QuerySet[Professor]:
    if (len(query) > 1):
        professors = {}
        sorted_professors = []
        all_professors = Professor.objects.all()
        for i in all_professors:
            if (fuzz.WRatio(query, i.name) >= PROFESSOR_RATIO or fuzz.token_sort_ratio(query, i.name) >= PROFESSOR_RATIO or fuzz.partial_ratio(query, i.name) >= PROFESSOR_RATIO):
                professors[i] = fuzz.WRatio(query, i.name)
        sorted_professors = sorted(professors, key=professors.get, reverse=True)
        return sorted_professors
    else:
        professors = Professor.objects.filter(
        Q(name__istartswith=f"{query} ")
        | Q(name__icontains=f" {query} ")
        | Q(name__iendswith=f" {query}")
        | Q(name__iexact=query)
        )
        return professors

def course_id_query(course_subject_code: str, catalog_number: str) -> Course:
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
        "course_subject_code": course.course_subject_code,
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


RESULT_FILTERS = [
    "UY",
    "GY",
    "y2021",
    "y2022",
]


def apply_result_filters(request: HttpRequest, unfiltered_courses: [dict]) -> [dict]:
    filtered_courses = []
    for course in unfiltered_courses:
        program = course["course_subject_code"].split("-")[1]
        last_offered = f"y{course['last_offered'].split(' ')[1]}"
        if program in request.POST and last_offered in request.POST:
            filtered_courses.append(course)
    return filtered_courses


def apply_filter_checkbox_values(request: HttpRequest, context: dict) -> None:
    for filter_value in RESULT_FILTERS:
        context[filter_value] = filter_value in request.POST
