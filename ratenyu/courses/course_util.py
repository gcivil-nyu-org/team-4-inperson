from typing import List
from json import dumps
from profanity_filter import ProfanityFilter
from django.http import HttpRequest
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Course, Class, Review
from professors.models import Professor
from courses.models import Course, Class
import re
import logging

LOGGER = logging.getLogger("project")

REVIEW_ADDED = "Your review was saved!"
REVIEW_CONTAINS_PROFANITY = "Profane review was not saved!"
REVIEW_NOT_SAVED = "Uh Oh, something went wrong. Your review could not be saved."


def create_review_objects_from_class(class_obj: Class) -> List[dict]:
    review_objects = []
    for review in Review.objects.filter(class_id=class_obj.class_id):
        review_objects.append(
            {
                "review_obj": review,
                "professor_obj": review.class_id.professor,
                "course_obj": review.class_id.course,
            }
        )
    return review_objects


def create_review_objects(classes: List[Class]) -> List[dict]:
    review_objects = []
    for class_obj in classes:
        review_objects += create_review_objects_from_class(class_obj)
    return review_objects


def calculate_rating_avg(reviews_list: List[dict]) -> float:
    if len(reviews_list) == 0:
        return float(0)
    rating_sum = 0
    for review in reviews_list:
        rating_sum += review["review_obj"].rating
    return round(rating_sum / len(reviews_list), 1)


def get_class(course_id: str, professor_name: str) -> str:
    course = Course.objects.get(course_id=course_id)
    professor = Professor.objects.get(name=professor_name)
    return_class = Class.objects.filter(course=course).get(professor=professor)
    return return_class


def save_new_review(
    user: User,
    user_entered_course_id: str,
    professor_name: str,
    review_rating: str,
    review_text: str,
) -> Review:
    course_subject_code, catalog_number = get_sub_code_and_cat_num(
        user_entered_course_id
    )
    course_id = course_id_query(course_subject_code, catalog_number).course_id
    class_obj = get_class(course_id=course_id, professor_name=professor_name)
    new_review = Review(
        review_text=review_text,
        rating=review_rating,
        class_id=class_obj,
        user=user,
        pub_date=timezone.now(),
    )
    new_review.save()
    return new_review


def course_id_query(course_subject_code: str, catalog_number: str) -> Class:
    course = Course.objects.get(
        course_subject_code=course_subject_code.upper(),
        catalog_number=catalog_number.upper(),
    )
    return course


def get_sub_code_and_cat_num(query: str) -> tuple:
    course_subject_code = re.search(r"^[a-zA-Z]+[-\s]?[uy|UY|gy|GY]{2}", query).group(0)
    if "-" not in course_subject_code:
        course_subject_code = course_subject_code.replace(" ", "-")
    catalog_number = re.search(r"[0-9]{4}", query).group(0)
    return course_subject_code, catalog_number


def text_is_valid(review_text: str) -> bool:
    """
    Review text moderation function
    Returns false if given text string contains profanity
    Else returns true
    """
    pf = ProfanityFilter()
    return pf.censor(review_text) == review_text


def add_review_from_details(request) -> tuple:
    """
    Adds a review to the database
    """
    LOGGER.debug(request.POST)
    course_id = request.POST["course_id"]
    professor_name = request.POST["add_review_professor_name"]
    review_rating = request.POST["review_rating"]
    review_text = request.POST["review_text"]
    if text_is_valid(review_text):
        try:
            new_review = Review(
                review_text=review_text,
                rating=review_rating,
                class_id=get_class(course_id, professor_name),
                user=request.user,
                pub_date=timezone.now(),
            )
            new_review.save()
            LOGGER.debug("Review saved successfully", review_text)
            return True, REVIEW_ADDED
        except Exception as e:
            LOGGER.exception(e)
            return False, REVIEW_NOT_SAVED
    else:
        LOGGER.debug("Review contains profanity", review_text)
        return False, REVIEW_CONTAINS_PROFANITY


def add_redirect_message(request: HttpRequest, message: str, success: bool) -> None:
    """
    add_redirect_message clears the current messages in the HttpRequest
    and adds a new message. The message type (success or error) is determined
    by the success argument.
    """
    storage = messages.get_messages(request)
    if len(storage) > 0:
        storage.used = True
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)


def get_courses_data_json() -> str:
    """
    creates a JSON string of course data to be consumed by front end
    javascript.
    """
    courses_data_list = [
        {
            "course_id": course.course_id,
            "course_title": course.course_title.replace("'", ""),
            "display_course_id": f"{course.course_subject_code} {course.catalog_number}",
            "professors": get_professors_for_course(course)
        }
        for course in Course.objects.all()
    ]
    return dumps(courses_data_list)


def get_professors_for_course(course: Course) -> List[Professor]:
    """
    creates an array of data objects containing Professor info
    for all Professors that teach a given Course
    """
    all_classes_for_course = Class.objects.filter(course=course)
    all_professors_for_course = [cl.professor for cl in all_classes_for_course]
    professors_data_list = [
        {
            "professor_id": professor.professor_id,
            "professor_name": professor.name.replace("'", "")
        } for professor in all_professors_for_course
    ]
    return professors_data_list


def get_professors_data_json() -> str:
    """
    creates a JSON string of professor data to be consumed by front end
    javascript. 
    """
    professors_data_list = [
        {
            "professor_id": professor.professor_id,
            "professor_name": professor.name.replace("'", ""),
            "courses": get_courses_for_professor(professor)
        } for professor in Professor.objects.all()
    ]
    return dumps(professors_data_list)


def get_courses_for_professor(professor: Professor) -> List[Course]:
    """
    creates an array of data objects containing Course info
    for all Courses taught by a given Professor
    """
    all_classes_for_professor = Class.objects.filter(professor=professor)
    all_courses_for_professor = [cl.course for cl in all_classes_for_professor]
    courses_data_list = [
        {
            "course_id": course.course_id,
            "course_title": course.course_title.replace("'", ""),
            "display_course_id": f"{course.course_subject_code} {course.catalog_number}"
        } for course in all_courses_for_professor
    ]
    return courses_data_list
