import re
from django.http import HttpRequest, Http404
from django.shortcuts import render
from courses.models import Course
from courses.views import course_detail


def index(request):
    return render(request, "search/index.html")


def course_result(request, course_name):
    return render(request, "search/courseResult.html")


def professor_result(request, professor_name):
    return render(request, "search/professorResult.html")


'''
This function is used in the search page.
A user can search course by id, professor name, or course name.
This function will redirect the search result to the corresponding page.
'''


def search_by_id_func(request: HttpRequest):
    try:
        search_by = request.GET['search_by']
        query = request.GET['query']
        print(search_by)
        print(query)
        if search_by == 'CourseID':
            try:
                course_subject_code = re.search(
                    r'^[a-zA-Z]{4}|^[a-zA-Z]{2}[-\s][a-zA-Z]{2}', query).group(0)
                if len(course_subject_code) == 4:
                    course_subject_code = course_subject_code[:2] + \
                        '-' + course_subject_code[2:]
                elif len(course_subject_code) == 5 and course_subject_code[2] == ' ':
                    course_subject_code = course_subject_code[:2] + \
                        '-' + course_subject_code[2:]
                catalog_number = re.search(r'[0-9]{4}', query).group(0)
                course_id = Course.objects.get(
                    course_subject_code=course_subject_code, catalog_number=catalog_number)
                return course_detail(request, course_id.course_id)
            except:
                raise Http404("Invalid Course ID")
        return render(request, "search/courseResult.html")
    except:
        raise Http404("Something went wrong")
