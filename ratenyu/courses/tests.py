from django.test import TestCase
from django.utils import timezone
from .models import Course
from .course_util import *
from professors.models import Professor


class CourseDetailHelpersTest(TestCase):
    def setUp(self) -> None:
        create_test_course()
        create_test_professor()
        create_test_class_1(
            course=Course.objects.get(pk="170776"),
            professor=Professor.objects.get(pk="1")
        )
        create_test_class_2(
            course=Course.objects.get(pk="170776"),
            professor=Professor.objects.get(pk="1")
        )
        create_test_review_1(Class.objects.get(pk="1"))
        create_test_review_2(Class.objects.get(pk="1"))

    def test_helper_functions(self) -> None:
        test_course = Course.objects.get(pk="170776")
        review_objects = create_review_objects(Class.objects.filter(course=test_course))
        self.assertEqual(2, len(review_objects), f"Expected 2 reviews, found {len(review_objects)}.")
        self.assertEqual(3.0, calculate_rating_avg(review_objects))


def create_test_course() -> Course:
    return Course.objects.create(
        course_id="170776",
        course_title="test course",
        course_subject_code="TS",
        catalog_number="1000",
        course_description="course_description"
    )


def create_test_professor() -> Professor:
    return Professor.objects.create(
        professor_id="1",
        name="John Doe",
        net_id="jd123",
        role="01"
    )


def create_test_class_1(course: Course, professor: Professor) -> Class:
    return Class.objects.create(
        class_id="1",
        professor=professor,
        course=course,
        class_type="Test",
        class_section="1",
        term="Jan2022",
        last_offered="Jan2022",
        location="WS",
        enroll_capacity=100
    )


def create_test_class_2(course: Course, professor: Professor) -> Class:
    return Class.objects.create(
        class_id="2",
        professor=professor,
        course=course,
        class_type="Test",
        class_section="2",
        term="Fall2023",
        last_offered="Fall2023",
        location="BK",
        enroll_capacity=50
    )


def create_test_review_1(class_id: Class) -> Review:
    return Review.objects.create(
        review_text="I love this professor!",
        rating=5,
        class_id=class_id,
        user="User1",
        pub_date=timezone.now()
    )


def create_test_review_2(class_id: Class) -> Review:
    return Review.objects.create(
        review_text="I hate this professor!",
        rating=1,
        class_id=class_id,
        user="User2",
        pub_date=timezone.now()
    )
