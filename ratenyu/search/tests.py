from django.test import TestCase, RequestFactory
from .search_util import *
from courses.models import Course
from courses.tests import create_test_course
from .views import *


class TestSearchPageRequests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        create_test_course()

    def testCourseNameRequest(self) -> None:
        request_str = f"/search?search_by=CourseName&query=Foundations"
        request = self.factory.get(request_str)
        response = search_by_select(request=request)
        self.assertEqual(
            200,
            response.status_code,
            f"Request returned {response.status_code} for request {request_str}",
        )

    def testCourseIDRequest(self) -> None:
        request_str = f"/search?search_by=CourseID&query=ts+uy+1000"
        request = self.factory.get(request_str)
        response = search_by_select(request=request)
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
