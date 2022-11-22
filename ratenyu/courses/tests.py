from django.test import TestCase, RequestFactory, Client
from .views import course_detail, add_review, delete_review
from .course_util import *
from professors.models import Professor
import users.tests as user_tests
import logging

logging.disable(logging.ERROR)


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
        create_test_review_easy()
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
        User.objects.create(username="hw2808", email="hw2808@nyu.edu")
        create_test_course()
        create_test_professor()
        create_test_class_1(
            course=Course.objects.get(pk="1"), professor=Professor.objects.get(pk="1")
        )

    def test_valid_request_get(self) -> None:
        request_str = f"http://127.0.0.1:8000/courses/add_review"
        request = self.factory.get(request_str)
        request.user = User.objects.get(pk=1)
        response = add_review(request=request)
        self.assertEqual(
            200,
            response.status_code,
            f"Request returned {response.status_code} for request {request_str}",
        )

    def test_valid_request_post(self) -> None:
        request_str = f"http://127.0.0.1:8000/courses/add_review"
        request_body = {
            "add_review_course_id": "TS-UY 1000",
            "add_review_professor_name": "John Doe",
            "review_rating": "5",
            "review_text": "Test Content",
        }
        request = self.factory.post(request_str, request_body)
        request._messages = messages.storage.default_storage(request)
        request.user = User.objects.get(pk=1)
        response = add_review(request)
        self.assertEqual(
            302,
            response.status_code,
            f"Request returned {response.status_code} for request {request_str}",
        )


class TestAddReviewPageHelpers(TestCase):
    def setUp(self) -> None:
        create_test_course()
        create_test_professor()
        create_test_class_1(
            course=Course.objects.get(pk="1"), professor=Professor.objects.get(pk="1")
        )
        self.factory = RequestFactory()

    def test_get_class(self):
        test_class = Class.objects.get(pk=1)
        found_class = get_class(1, "John Doe")
        self.assertEqual(test_class.class_id, found_class.class_id)

    def test_save_review(self):
        user = User.objects.create(username="test", email="test@nyu.edu")
        course_id = "TS-UY 1000"
        professor_name = "John Doe"
        review_rating = "5"
        review_text = "test"
        r = save_new_review(
            user=user,
            user_entered_course_id=course_id,
            professor_name=professor_name,
            review_rating=review_rating,
            review_text=review_text,
        )
        self.assertEqual(r, Review.objects.get(pk=1))


class TestReviewTextValidation(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.review_text_invalid = "This teacher is a bitch."
        self.review_text_valid = "I do not like this teacher."
        User.objects.create(username="testuser", email="testuser@nyu.edu")
        create_test_course()
        create_test_professor()
        create_test_class_1(
            course=Course.objects.get(pk="1"), professor=Professor.objects.get(pk="1")
        )

    def test_validation_function(self):
        self.assertFalse(text_is_valid(self.review_text_invalid))
        self.assertTrue(text_is_valid(self.review_text_valid))

    def test_invalid_review_submission(self) -> None:
        request_str = f"http://127.0.0.1:8000/courses/add_review"
        request_body = {
            "add_review_course_id": "TS-UY 1000",
            "add_review_professor_name": "John Doe",
            "review_rating": "5",
            "review_text": "Shit is a bad word",
        }
        request = self.factory.post(request_str, request_body)
        request._messages = messages.storage.default_storage(request)
        request.user = User.objects.get(pk=1)
        response = add_review(request)
        cl = Class.objects.get(pk=1)
        self.assertEqual(0, len(Review.objects.filter(class_id=cl)), "Profane review was saved!")


class TestReviewFromDetailsPage(TestCase):
    def setUp(self):
        user_tests.create_test_course()
        user_tests.create_test_professor()
        user_tests.create_test_user()
        user_tests.create_test_class_1(
            course=Course.objects.get(pk="1"), professor=Professor.objects.get(pk="1")
        )
        user_tests.create_test_review_1(Class.objects.get(pk="1"), User.objects.get(username="viren"))
        user_tests.create_test_review_2(Class.objects.get(pk="1"), User.objects.get(username="viren"))
        self.factory = RequestFactory()
        self.client = Client()
        return super().setUp()
    
    def test_review_from_details_page_1(self):
        self.client.login(username="viren", password="viren")
        request_str = f"http://127.0.0.1:8000/courses/1"
        response = self.client.post(request_str, {"course_id":"1","add_review_professor_name":"John Doe", "review_text": "This is a test review", "review_rating": "5", "submit":""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is a test review")
        self.assertContains(response, "5.0")
        self.assertContains(response, REVIEW_ADDED)

    def test_review_from_details_page_2(self):
        self.client.login(username="viren", password="viren")
        request_str = f"http://127.0.0.1:8000/courses/1"
        response = self.client.post(request_str, {"course_id":"1","add_review_professor_name":"John Doe", "review_text": "Shit is a abd word", "review_rating": "5", "submit":""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Review not saved. Review text failed to meet RateNYU standards.")
    
    def test_review_from_details_page_3(self):
        self.client.login(username="viren", password="viren")
        request_str = f"http://127.0.0.1:8000/courses/1"
        response = self.client.post(request_str, {"course_id":"1","add_review_professor_name":"Different Professor", "review_text": "This is a test review", "review_rating": "6", "submit":""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, REVIEW_NOT_SAVED)

    def test_review_from_details_page_4(self):
        self.client.login(username="viren", password="viren")
        request_str = f"http://127.0.0.1:8000/courses/1"
        response = self.client.post(request_str, {"course_id":"1","add_review_professor_name":"John Doe", "review_text": "This is a test review", "review_rating": "6"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid request")

    def test_pagination(self):
        self.client.login(username="viren", password="viren")
        request_str = f"http://127.0.0.1:8000/courses/1?page=thisIsTheTestForPageNumberNotInt"
        response = self.client.post(request_str, {"course_id":"1","add_review_professor_name":"John Doe", "review_text": "This is a test review1", "review_rating": "4", "submit":""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is a test review1")
        self.assertContains(response, "4.0")


class TestDeleteReview(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_delete_review(self):
        review = create_test_review_easy()
        self.assertEqual(1, len(Review.objects.filter(pk=review.id)), "Test Review was not created.")
        url = f"http://127.0.0.1:8000/courses/{review.id}/delete"
        request = self.factory.get(url)
        delete_review(request, str(review.id))
        self.assertEqual(0, len(Review.objects.filter(pk=review.id)), "Test Review was not deleted.")


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


def create_test_review_easy() -> Review:
    create_test_course()
    create_test_professor()
    create_test_class_1(
        course=Course.objects.get(pk="1"), professor=Professor.objects.get(pk="1")
    )
    create_test_class_2(
        course=Course.objects.get(pk="1"), professor=Professor.objects.get(pk="1")
    )
    return create_test_review_1(Class.objects.get(pk="1"))
