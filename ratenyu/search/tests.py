from django.test import TestCase, RequestFactory
from .search_util import *
from courses.models import Course
from .views import search_by_course_name, search_by_select


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
        self.assertEqual(
            int(course_query(query)[0].course_id), int(course.course_id))

    def test_non_matching_course_name_query(self) -> None:
        """if a query is valid, it should return courses which contain the query"""
        query = "Software"
        self.assertQuerysetEqual(course_query(query), [])


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
        """if a valid course id is passed, it should return the course details page """
        #request_str = f"search?search_by=CourseID&query=BT-GY6093"
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
        """if a valid course id is passed, it should return the course details page """
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
