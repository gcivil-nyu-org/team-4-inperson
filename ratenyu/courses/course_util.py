from typing import List
from .models import Class, Review, Course


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


def get_course_last_offered_term(course: Course) -> str:
    all_classes = Class.objects.filter(course=course)
    return max(all_classes.only("last_offered"))
