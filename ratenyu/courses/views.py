from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, Http404
from .models import Course, Class, Review
from professors.models import Professor


# Create your views here.
def class_detail(request: HttpRequest, class_id: str):
    try:
        classes = Class.objects.get(pk=class_id)
        course = Course.objects.get(course_id=classes.course.course_id)
        professor = Professor.objects.get(pk=classes.professor.professor_id)
        reviews = Review.objects.filter(class_id=class_id)
        classes_pro = Class.objects.filter(course=course.course_id)
        professor_list = []
        reviews_list = []
        reviews_rating_list = []
        for cls in classes_pro:
            if cls.professor.name not in professor_list:
                professor_list.append(cls.professor.name)
        for rev in reviews:
            current_review = {
                'review_obj': rev,
                'course_obj': course,
            }
            reviews_list.append(current_review)
            reviews_rating_list.append(rev.rating)
        if len(reviews_rating_list) > 0:
            reviews_avg = round(float(sum(reviews_rating_list)/len(reviews_rating_list)), 1)
        else:
            reviews_avg = 0
        context = {
            'classes': classes,
            'course': course,
            'professor': professor,
            'reviews_list': reviews_list,
            'reviews_avg': reviews_avg,
            'professor_list': professor_list,
        }
        return render(request, "courses/detail.html", context)
    except Class.DoesNotExist:
        raise Http404("Class does not exist")
