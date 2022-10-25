from django.test import TestCase, RequestFactory
from .models import Professor
from .views import professor_detail


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
        self.assertEqual(200, response.status_code, f"Request returned {response.status_code} for request {request_str}")


def create_test_professor() -> Professor:
    return Professor.objects.create(
        professor_id="1",
        name="John Doe",
        net_id="jd123",
        role="01"
    )
