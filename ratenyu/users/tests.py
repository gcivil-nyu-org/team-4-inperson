from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from courses.models import Course, Review, Class
from professors.models import Professor
from users.models import UserDetails

class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse("users:register")
        User.objects.create(username="hw2807", email="hw2807@nyu.edu")
        self.user = {
            "name": "Haofan Wang",
            "email": "hw2807@nyu.edu",
            "username": "HaofanWang",
            "password1": "fnewkjfwgjee23234.",
            "password2": "fnewkjfwgjee23234.",
            "major": "Computer Science",
            "student_status": "Master2",
        }
        return super().setUp()


class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user)
        self.assertEqual(response.status_code, 302)


class TestProfilePage(TestCase):

    def setUp(self) -> None:
        create_test_course()
        create_test_professor()
        create_test_user()
        create_test_class_1(
            course=Course.objects.get(pk="1"), professor=Professor.objects.get(pk="1")
        )
        create_test_review_1(Class.objects.get(pk="1"), User.objects.get(username="viren"))
        create_test_review_2(Class.objects.get(pk="1"), User.objects.get(username="viren"))
        return super().setUp()
    
    def test_profile_page_1(self):
        '''
        A user is logged in and user is loading their own profile page
        The profile page should load the details of the user and 
        '''
        self.client.login(username="viren", password="viren")
        response = self.client.get(reverse("users:profile", args=["viren"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")
        self.assertContains(response, "Viren Parmar")
        self.assertContains(response, "Computer Science")
        self.assertContains(response, "Master2")
        self.assertContains(response, "test course")
        self.assertContains(response, "John Doe")
        self.assertContains(response, "I love this professor!")
        self.assertContains(response, "I love this professor!")
        
    def test_profile_page_2(self):
        '''
        A user is logged in and user is loading someone else's profile page
        This should fail as user is not allowed to view other's profile page
        '''
        self.client.login(username="viren", password="viren")
        response = self.client.get(reverse("users:profile", args=["otheruser"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "error.html")
        self.assertContains(response, "You are not authorized to view this page.")

    def test_profile_page_3(self):
        '''
        A user is not logged in and user is loading proflie page.
        This should fail and redirect to the search page
        '''
        response = self.client.get(reverse("users:profile", args=["viren"]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("search:index"))
        


def create_test_course() -> Course:
    Course.objects.create(
        course_id="1",
        course_title="test course",
        course_subject_code="TS-UY",
        catalog_number="1000",
        course_description="course_description",
    )

def create_test_professor() -> Professor:
    Professor.objects.create(
        professor_id="1", name="John Doe", net_id="jd123", role="01"
    )

def create_test_user() -> User:
    user = User.objects.create(username="viren", email="vmp2018@nyu.edu")
    user.set_password("viren")
    user.save()
    UserDetails.objects.create(user=user, name="Viren Parmar", major="Computer Science", student_status="Master2")



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


def create_test_review_1(class_id: Class, user: User) -> Review:
    return Review.objects.create(
        review_text="I love this professor!",
        rating=5,
        class_id=class_id,
        user=user,
        pub_date=timezone.now(),
    )


def create_test_review_2(class_id: Class, user: User) -> Review:
    return Review.objects.create(
        review_text="I hate this professor!",
        rating=1,
        class_id=class_id,
        user=user,
        pub_date=timezone.now(),
    )