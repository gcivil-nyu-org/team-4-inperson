from django.test import TestCase, RequestFactory
from .search_util import *
from courses.models import Course, Class
from professors.models import Professor
from .views import search_by_course_name
from courses.tests import *


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

class TestSearchPageHelpers(TestCase):
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

    def test_course_helper_function(self) -> None:
        test_course = Course.objects.get(pk="1")
        d = get_course_results_info(test_course)
        self.assertEqual(2, len(d['reviews_list']))
        self.assertEqual(3.0, d['reviews_avg'])

    def test_professor_helper_function(self) -> None:
        test_professor = Professor.objects.get(pk="1")
        d = get_professor_results_info(test_professor)
        self.assertEqual(2, len(d['reviews_list']))
        self.assertEqual(3.0, d['reviews_avg'])
