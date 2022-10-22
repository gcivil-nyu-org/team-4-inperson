from django.shortcuts import render
from django.http import HttpRequest, Http404
from courses.models import Course
from professors.models import Professor


def index(request):
    return render(request, "search/index.html")


def course_result(request, course_name):
    return render(request, "search/courseResult.html")


def professor_result(request, professor_name):
    return render(request, "search/professorResult.html")


def search_by_select(request: HttpRequest):
    search_by = request.GET['search_by']
    if search_by == 'CourseID':
        return search_by_course_id(request)
    elif search_by == 'CourseName':
        return search_by_course_name(request)
    elif search_by == 'ProfessorName':
        return search_by_professor_name(request)

def search_by_course_id(request: HttpRequest):
    return render(request, 'search/courseResult.html')

def search_by_course_name(request: HttpRequest):
    query = request.GET['query']
    courses = Course.objects.filter(course_title__contains=query)
    context = {'courses':  courses}
    return render(request, 'search/courseResult.html', context)

def search_by_professor_name(request):
    query = request.GET['query']
    professors = Professor.objects.filter(name__contains=query)
    context = {'professors':  professors}
    return render(request, 'search/professorResult.html', context)


