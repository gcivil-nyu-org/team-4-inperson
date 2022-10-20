from django.test import TestCase

from .models import Professor


class ProfessorCreateTest(TestCase):
    def setUp(self) -> None:
        Professor.objects.create(
            professor_id="1",
            name="John Doe",
            net_id="jd123",
            role="Test Role"
        )

    def testProfessorCreate(self) -> None:
        professor = Professor.objects.get(professor_id="1")
        self.assertEqual(professor.name, "John Doe", "Failed to create test professor.")

