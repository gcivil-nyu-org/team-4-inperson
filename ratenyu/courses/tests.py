from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Course, Review
from .views import course_detail, add_review
from .course_util import *
from professors.models import Professor


class TestHomePage(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()


class TestCourseDetailPageRequest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        create_test_course()

    def testCourseCreated(self) -> None:
        course = Course.objects.get(pk="1")
        self.assertIsInstance(course, Course, "Test course not created.")

    def testValidRequest(self) -> None:
        course_id = "1"
        request_str = f"http://127.0.0.1:8000/courses/{course_id}"
        request = self.factory.get(request_str)
        response = course_detail(request=request, course_id=course_id)
        self.assertEqual(
            200,
            response.status_code,
            f"Request returned {response.status_code} for request {request_str}",
        )


class TestDetailPageHelpers(TestCase):
    def setUp(self) -> None:
        create_test_course()
        create_test_professor()
        create_test_class_1(
            course=Course.objects.get(pk="1"), professor=Professor.objects.get(pk="1")
        )
        create_test_class_2(
            course=Course.objects.get(pk="1"), professor=Professor.objects.get(pk="1")
        )
        create_test_review_1(Class.objects.get(pk="1"))
        create_test_review_2(Class.objects.get(pk="1"))

    def test_helper_functions(self) -> None:
        test_course = Course.objects.get(pk="1")
        review_objects = create_review_objects(Class.objects.filter(course=test_course))
        self.assertEqual(
            2, len(review_objects), f"Expected 2 reviews, found {len(review_objects)}."
        )
        self.assertEqual(3.0, calculate_rating_avg(review_objects))

class TestAddReviewPage(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()
    def testValidRequestGet(self) -> None:
        user = User.objects.create(username="hw2808", email="hw2808@nyu.edu")
        request_str = f"http://127.0.0.1:8000/courses/add_review"
        request = self.factory.get(request_str)
        request.user = User.objects.get(pk=1)
        response = add_review(request=request)
        self.assertEqual(
            200,
            response.status_code,
            f"Request returned {response.status_code} for request {request_str}",
        )

    def testValidRequestPost(self) -> None:
        user = User.objects.create(username="hw2808", email="hw2808@nyu.edu")
        request_str = f"http://127.0.0.1:8000/courses/add_review"
        request = self.factory.post(request_str, {'user': user,'add_review_course_id': ' CS-GY 6003 ',
                                                  'add_review_professor_name': ' Erin McLeish ','review_rating': ' 5 ',
                                                 'review_text': ' Great '})
        request.user = User.objects.get(pk=1)
        response = add_review(request)
        self.assertEqual(
            200,
            response.status_code,
            f"Request returned {response.status_code} for request {request_str}",
        )

    # def test_save_review(self):
    #     user = User.objects.create(username="hw2808", email="hw2808@nyu.edu")
    #     course_id = ' CS-GY 6063 '
    #     professor_name = ' Gennadiy Civil '
    #     review_rating = ' 5 '
    #     review_text = ' test '
    #     r = save_new_review(user=user,
    #             user_entered_course_id=course_id,
    #             professor_name=professor_name,
    #             review_rating=review_rating,
    #             review_text=review_text)
    #     # self.assertEqual(r, Review.objects.get(pk=1))

def create_test_course() -> Course:
    return Course.objects.create(
        course_id="1",
        course_title="test course",
        course_subject_code="TS-UY",
        catalog_number="1000",
        course_description="course_description",
    )


def create_test_professor() -> Professor:
    return Professor.objects.create(
        professor_id="1", name="John Doe", net_id="jd123", role="01"
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
        enroll_capacity=100,
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
        enroll_capacity=50,
    )


def create_test_review_1(class_id: Class) -> Review:
    user = User.objects.create(username="hw2807", email="hw2807@nyu.edu")
    return Review.objects.create(
        review_text="I love this professor!",
        rating=5,
        class_id=class_id,
        user=user,
        pub_date=timezone.now(),
    )


def create_test_review_2(class_id: Class) -> Review:
    user = User.objects.create(username="hw2808", email="hw2808@nyu.edu")
    return Review.objects.create(
        review_text="I hate this professor!",
        rating=1,
        class_id=class_id,
        user=user,
        pub_date=timezone.now(),
    )

def login(self):
    self.username
