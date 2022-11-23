from django.test import TestCase, RequestFactory, Client
from .models import Professor
from .views import professor_detail
from courses.models import Course, Class
from users.models import User
import users.tests as user_tests
from courses.course_util import REVIEW_ADDED, REVIEW_NOT_SAVED
import logging

logging.disable(logging.ERROR)


class TestProfessorDetailPageRequest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        create_test_professor()

    def testProfessorCreated(self) -> None:
        professor = Professor.objects.get(pk="1")
        self.assertIsInstance(professor, Professor, "Test professor not created.")

    def testValidRequest(self) -> None:
        professor_id = "1"
        request_str = f"http://127.0.0.1:8000/professors/{professor_id}"
        request = self.factory.get(request_str)
        response = professor_detail(request=request, professor_id=professor_id)
        self.assertEqual(
            200,
            response.status_code,
            f"Request returned {response.status_code} for request {request_str}",
        )

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
        request_str = f"http://127.0.0.1:8000/professors/1"
        response = self.client.post(request_str, {"course_id":"1","add_review_professor_name":"John Doe", "review_text": "This is a test review", "review_rating": "5", "submit":""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is a test review")
        self.assertContains(response, "5.0")
        self.assertContains(response, REVIEW_ADDED)

    def test_review_from_details_page_2(self):
        self.client.login(username="viren", password="viren")
        request_str = f"http://127.0.0.1:8000/professors/1"
        response = self.client.post(request_str, {"course_id":"1","add_review_professor_name":"John Doe", "review_text": "Shit is a abd word", "review_rating": "5", "submit":""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Review not saved. Review text failed to meet RateNYU standards.")
    
    def test_review_from_details_page_3(self):
        self.client.login(username="viren", password="viren")
        request_str = f"http://127.0.0.1:8000/professors/1"
        response = self.client.post(request_str, {"course_id":"1","add_review_professor_name":"Different Professor", "review_text": "This is a test review", "review_rating": "6", "submit":""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, REVIEW_NOT_SAVED)

    def test_review_from_details_page_4(self):
        self.client.login(username="viren", password="viren")
        request_str = f"http://127.0.0.1:8000/professors/1"
        response = self.client.post(request_str, {"course_id":"1","add_review_professor_name":"John Doe", "review_text": "This is a test review", "review_rating": "6"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid request")

def create_test_professor() -> Professor:
    return Professor.objects.create(
        professor_id="1", name="John Doe", net_id="jd123", role="01"
    )
