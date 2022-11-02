from django.test import TestCase, RequestFactory
from .search_util import *
from courses.models import Course, Class
from professors.models import Professor
from .views import (
    search_by_course_name,
    search_by_professor_name,
    index,
    search_by_select,
)
from courses.tests import *


# Create your tests here.


class TestSearchPageRequest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def testValidRequest(self) -> None:
        request = self.factory.get(f"search")
        response = index(request)
        self.assertEqual(200, response.status_code)


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
        response = search_by_professor_name(request=request)
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
        professor = Professor(professor_id=1, name="John Smith", net_id="1", role="1")
        professor.save()
        self.assertEqual(
            int(professor_query(query)[0].professor_id), int(professor.professor_id)
        )

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
        self.assertEqual(test_course, d["course_obj"])
        self.assertEqual(2, len(d["reviews_list"]))
        self.assertEqual(3.0, d["reviews_avg"])

    def test_professor_helper_function(self) -> None:
        test_professor = Professor.objects.get(pk="1")
        d = get_professor_results_info(test_professor)
        self.assertEqual(test_professor, d["professor_obj"])
        self.assertEqual(2, len(d["reviews_list"]))
        self.assertEqual(3.0, d["reviews_avg"])


class TestCourseIdSearch(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.course = Course(
            course_id=1,
            course_title="Biomedical Materials & Devices for Human Body Repair",
            course_subject_code="BT-GY",
            catalog_number="6093",
            course_description="The main objective of this multidisciplinary course is to provide students with a broad survey of currently used biomaterials and their use in medical devices for reconstructing or replacing injured, diseased, or aged human tissues and organs. Topics include a broad introduction to the materials used in medicine and their chemical, physical, and biological properties, basic mechanisms of wound healing and materials-tissue interactions. | Advisor/Instructor Permission Required",
        )
        self.course.save()
        self.courseId = "BT-GY 6093"

    def test_valid_course_id_case_1(self) -> None:
        """if a valid course id is passed, it should return the course details page"""
        # request_str = f"search?search_by=CourseID&query=BT-GY6093"
        # Testing the get view for search_by_select
        request_str = f"search/search?search_by=CourseID&query=BT-GY6093"
        request = self.factory.get(request_str)
        response = search_by_select(request=request)
        self.assertEqual(
            200,
            response.status_code,
            f"Request returned {response.status_code} for request {request_str}",
        )
        self.assertContains(response, self.courseId)

    def test_valid_course_id_case_2(self) -> None:
        """if a valid course id is passed, it should return the course details page"""
        # Testing the get view for search_by_course_id
        request_str = f"search/search?search_by=CourseID&query=BT-GY 6093"
        request = self.factory.get(request_str)
        response = search_by_select(request=request)
        self.assertEqual(
            200,
            response.status_code,
            f"Request returned {response.status_code} for request {request_str}",
        )
        self.assertContains(response, self.courseId)

    def test_invalid_course_id(self) -> None:
        """if an invalid course id is passed, it should return the search page with no results"""
        request_str = f"search/search?search_by=CourseID&query=VIP-GY 6094"
        request = self.factory.get(request_str)
        response = search_by_select(request=request)
        self.assertEqual(
            200,
            response.status_code,
            f"Request returned {response.status_code} for request {request_str}",
        )
        self.assertContains(response, "CourseID not found")

    def test_no_course_id(self) -> None:
        """if no course id is passed, it should return the search page with no results"""
        request_str = f"search/search?search_by=CourseID&query="
        request = self.factory.get(request_str)
        response = search_by_select(request=request)
        self.assertEqual(
            200,
            response.status_code,
            f"Request returned {response.status_code} for request {request_str}",
        )
        self.assertContains(response, "Something went wrong")
