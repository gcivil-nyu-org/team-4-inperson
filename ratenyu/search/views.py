from django.shortcuts import render
from django.http import HttpRequest, Http404
from django.db.models import Q
from courses.models import Course, Class, Review
from professors.models import Professor


def index(request):
    return render(request, "search/index.html")


def search_by_select(request: HttpRequest):
    search_by = request.GET["search_by"]
    if search_by == "CourseID":
        return search_by_course_id(request)
    elif search_by == "CourseName":
        return search_by_course_name(request)
    elif search_by == "ProfessorName":
        return search_by_professor_name(request)


def search_by_course_id(request: HttpRequest):
    return render(request, "search/courseResult.html")


def search_by_course_name(request: HttpRequest):
    try:
        query = request.GET["query"]
        courses = Course.objects.filter(
            Q(course_title__startswith=f"{query} ") |
            Q(course_title__contains=f" {query} ") |
            Q(course_title__endswith=f" {query}") |
            Q(course_title=query)
        )

        filtered_courses = []
        for i in courses:
            reviews_list = []
            reviews_rating_list = []
            classes = Class.objects.filter(course=i.course_id)
            for cl in classes:
                review_set = Review.objects.filter(class_id=cl.class_id)
                for rev in review_set:
                    current_review = {
                        "review_obj": rev
                    }
                    reviews_list.append(current_review)
                    reviews_rating_list.append(rev.rating)
            if len(reviews_rating_list) > 0:
                reviews_avg = round(
                    float(sum(reviews_rating_list) / len(reviews_rating_list)), 1
                )
            else:
                reviews_avg = 0

            current_course = {
                    "course_id": i.course_id,
                    "course_title":i.course_title,
                    "course_subject_code":i.course_subject_code,
                    "catalog_number":i.catalog_number,
                    "course_description":i.course_description,
                    "reviews_list":reviews_list,
                    "reviews_avg":reviews_avg
                }

            filtered_courses.append(current_course)
        context = {
            "courses":  filtered_courses,
            "query" : query,
        }
        return render(request, "search/courseResult.html", context)
    except:
        raise Http404("Something went wrong")


def search_by_professor_name(request):
    try:
        query = request.GET["query"]
        professors = Professor.objects.filter(
            Q(name__startswith=f"{query} ") |
            Q(name__contains=f" {query} ") |
            Q(name__endswith=f" {query}")
        )
        context = {"professors":  professors}
        return render(request, "search/professorResult.html", context)
    except:
        raise Http404("Something went wrong")

