from django.test import TestCase, RequestFactory
from .search_util import *
from courses.models import Course
from professors.models import Professor
from .views import search_by_course_name


# Create your tests here.


class TestCourseResultsPageRequest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def testValidRequest(self) -> None:
        course_id = "1"
        request_str = f"search/search?search_by=CourseName&query=Foundations"
        request = self.factory.get(request_str)
        response = search_by_course_name(request=request)
        self.assertEqual(
            200,
            response.status_code,
            f"Request returned {response.status_code} for request {request_str}",
        )

class TestProfessorResultsPageRequest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def testValidReqeust(self) -> None:
        request_str = f"search/search?search_by=ProfessorName&query=John"
        request = self.factory.get(request_str)
        response = search_by_course_name(request=request)
        self.assertEqual(
            200,
            response.status_code,
            f"Request returned {response.status_code} for request {request_str}",
        )



class TestSearchFiltering(TestCase):
    def test_matching_course_name_query(self) -> None:
        """if a query is valid, it should return courses which contain the query"""
        query = "Software"
        course = Course(
            course_id=1,
            course_title="Software Engineering",
            course_subject_code="1",
            catalog_number="1",
            course_description="abc",
        )
        course.save()
        self.assertEqual(int(course_query(query)[0].course_id), int(course.course_id))

    def test_non_matching_course_name_query(self) -> None:
        """if a query is valid, it should return courses which contain the query"""
        query = "Software"
        self.assertQuerysetEqual(course_query(query), [])

    def test_matching_professor_name_query(self) -> None:
        query = "John"
        professor = Professor(professor_id=1,
                              name="John Smith",
                              net_id="1",
                              role="1"
                              )
        professor.save()
        self.assertEqual(int(professor_query(query)[0].professor_id),int(professor.professor_id))

    def test_non_matching_professor_name_query(self) -> None:
        query = "John"
        self.assertQuerysetEqual(professor_query(query), [])