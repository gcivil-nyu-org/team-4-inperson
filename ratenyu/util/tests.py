from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from professors.models import Professor
from courses.models import Course, Class, Vote, Review
from users.models import User

import users.tests as user_tests

# Create your tests here.

class TestVotes(TestCase):
    def setUp(self) -> None:
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
    
    def test_like_when_no_vote_present(self):
        self.client.login(username="viren", password="viren")
        response = self.client.post(reverse("courses:like_review", args=["1"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vote.objects.get(pk="1").vote, "L")
        self.assertEqual(Vote.objects.get(pk="1").review, Review.objects.get(pk="1"))
        self.assertEqual(Vote.objects.get(pk="1").user, User.objects.get(username="viren"))
    
    def test_like_when_vote_like_present(self):
        self.client.login(username="viren", password="viren")
        Vote.objects.get_or_create(pk="1", review=Review.objects.get(pk="1"), user=User.objects.get(username="viren"), vote="L")
        self.client.post(reverse("courses:like_review", args=["1"]))
        response = self.client.post(reverse("courses:like_review", args=["1"]))
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Vote.DoesNotExist): 
            Vote.objects.get(id="1")
    
    def test_like_when_vote_dislike_present(self):
        self.client.login(username="viren", password="viren")
        self.client.post(reverse("courses:dislike_review", args=["1"]))
        Vote.objects.get_or_create(pk="1", review=Review.objects.get(pk="1"), user=User.objects.get(username="viren"), vote="D")
        response = self.client.post(reverse("courses:like_review", args=["1"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vote.objects.get(pk="1").vote, "L")
        self.assertEqual(Vote.objects.get(pk="1").review, Review.objects.get(pk="1"))
        self.assertEqual(Vote.objects.get(pk="1").user, User.objects.get(username="viren"))

    def test_dislike_when_no_vote_present(self):
        self.client.login(username="viren", password="viren")
        response = self.client.post(reverse("courses:dislike_review", args=["1"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vote.objects.get(pk="1").vote, "D")
        self.assertEqual(Vote.objects.get(pk="1").review, Review.objects.get(pk="1"))
        self.assertEqual(Vote.objects.get(pk="1").user, User.objects.get(username="viren"))
    
    def test_dislike_when_vote_dislike_present(self):
        self.client.login(username="viren", password="viren")
        Vote.objects.get_or_create(pk="1", review=Review.objects.get(pk="1"), user=User.objects.get(username="viren"), vote="D")
        self.client.post(reverse("courses:dislike_review", args=["1"]))
        response = self.client.post(reverse("courses:dislike_review", args=["1"]))
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Vote.DoesNotExist): 
            Vote.objects.get(id="1")
        
    
    def test_dislike_when_vote_like_present(self):
        self.client.login(username="viren", password="viren")
        Vote.objects.get_or_create(pk="1", review=Review.objects.get(pk="1"), user=User.objects.get(username="viren"), vote="L")
        response = self.client.post(reverse("courses:dislike_review", args=["1"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vote.objects.get(pk="1").vote, "D")
        self.assertEqual(Vote.objects.get(pk="1").review, Review.objects.get(pk="1"))
        self.assertEqual(Vote.objects.get(pk="1").user, User.objects.get(username="viren"))
    
    def test_like_with_error(self):
        self.client.login(username="viren", password="viren")
        response = self.client.post(reverse("courses:like_review", args=["3"]))
        self.assertEqual(response.status_code, 500)
    
    def test_dislike_with_error(self):
        self.client.login(username="viren", password="viren")
        response = self.client.post(reverse("courses:dislike_review", args=["3"]))
        self.assertEqual(response.status_code, 500)
        

    def tearDown(self) -> None:
        return super().tearDown()
