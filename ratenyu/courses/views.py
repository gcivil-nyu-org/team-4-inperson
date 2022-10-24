from django.shortcuts import render
from django.http import HttpRequest, Http404
from .models import Course, Class, Review


def course_detail(request: HttpRequest, course_id: str):
    try:
        course = Course.objects.get(course_id=course_id)
        classes = Class.objects.filter(course=course)
        professors_list = []
        for cl in classes:
            professors_list.append(cl.professor)
        reviews_list = []
        reviews_rating_list = []
        professor_link = "/professors/"
        for cl in classes:
            review_set = Review.objects.filter(class_id=cl.class_id)
            for rev in review_set:
                current_review = {
                    "review_obj": rev,
                    "professor_obj": cl.professor,
                    "professor_link": professor_link + cl.professor.professor_id,
                }
                reviews_list.append(current_review)
                reviews_rating_list.append(rev.rating)
        if len(reviews_rating_list) > 0:
            reviews_avg = round(
                float(sum(reviews_rating_list) / len(reviews_rating_list)), 1
            )
        else:
            reviews_avg = 0
        context = {
            "classes": classes,
            "course": course,
            "reviews_list": reviews_list,
            "reviews_avg": reviews_avg,
            "professors_list": professors_list,
        }
        return render(request, "courses/detail.html", context)
    except Course.DoesNotExist:
        raise Http404("Class does not exist")
