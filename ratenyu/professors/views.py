from django.shortcuts import render
from django.http import HttpRequest, Http404
from .models import Professor
from courses.models import Class, Course, Review


def professor_detail(request: HttpRequest, professor_id: int):
    try:
        professor = Professor.objects.get(pk=professor_id)
        classes = Class.objects.filter(professor_id=professor_id)
        courses_list = []
        for cl in classes:
            courses_list.append(cl.course)
        reviews_list = []
        reviews_rating_list = []
        course_link = "/courses/"
        for cl in classes:
            review_set = Review.objects.filter(class_id=cl.class_id)
            for rev in review_set:
                current_review = {
                    'review_obj': rev,
                    'course_obj': Course.objects.get(pk=cl.course_id),
                    'course_link': course_link + cl.course_id,
                }
                reviews_list.append(current_review)
                reviews_rating_list.append(rev.rating)
        if len(reviews_rating_list) > 0:
            reviews_avg = round(float(sum(reviews_rating_list)/len(reviews_rating_list)), 1)
        else:
            reviews_avg = 0
        context = {
            'professor': professor,
            'courses_list': courses_list,
            'reviews_list': reviews_list,
            'reviews_avg': reviews_avg
        }
        return render(request, "professors/detail.html", context)
    except Professor.DoesNotExist:
        raise Http404("Professor does not exist")
