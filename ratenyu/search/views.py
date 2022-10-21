from django.shortcuts import render


def index(request):
    return render(request, "search/index.html")


def course_result(request, course_name):
    return render(request, "search/courseResult.html")


def professor_result(request, professor_name):
    return render(request, "search/professorResult.html")
