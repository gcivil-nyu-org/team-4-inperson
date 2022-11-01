from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse("users:register")
        self.user = {
            'name': 'Haofan Wang',
            'email': 'hw2807@nyu.edu',
            'username': 'HaofanWang',
            'password1': 'fnewkjfwgjee23234.',
            'password2': 'fnewkjfwgjee23234.',
            'major': 'Computer Science',
            'student_status': 'Master2',
        }
        return super().setUp()


class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user)
        self.assertEqual(response.status_code, 302)

