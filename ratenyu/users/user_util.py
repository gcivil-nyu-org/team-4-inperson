
from django.contrib.auth.models import User
from .models import UserDetails
from util.views import error404
from courses.models import Review
import logging

logger = logging.getLogger("project")

def get_user_details(user_name: str) -> UserDetails:
    try:
        logger.debug(f"get_user_details({user_name})")
        user = User.objects.get(username=user_name)
        user_detail = UserDetails.objects.get(user=user)
        logger.debug(f"user_details : {user_detail}")
        return user_detail
    except Exception as e:
        logger.error(f"get_user_details({user_name}) : {e}")
        return None

def get_reviews_by_user(user_name: str) -> list:
    try:
        logger.debug(f"get_reviews_by_user({user_name})")
        review_objects = []
        for review in Review.objects.filter(user = User.objects.get(username=user_name)):
            review_objects.append(
                {
                    "review_obj": review,
                    "professor_obj": review.class_id.professor,
                    "course_obj": review.class_id.course,
                }
            )
        logger.debug(f"reviews : {review_objects}")
        return review_objects
    except Exception as e:
        logger.error(f"get_reviews_by_user({user_name}) : {e}")
        return None