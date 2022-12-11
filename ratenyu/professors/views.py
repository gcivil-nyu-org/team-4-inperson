from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Professor
from courses.models import Class, Course, Review
from util.models import Vote
from courses.course_util import *
from util.views import error404, util_like_review, util_dislike_review
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import logging

LOGGER = logging.getLogger("project")


def professor_detail(request: HttpRequest, professor_id: str):
    LOGGER.debug(f"professor_detail: {professor_id}")
    try:
        if request.method == "GET":
            rev_sorting = request.GET.get('rev-sorting')
            if rev_sorting is None:
                return load_professor_detail(request, professor_id)
            else:
                return load_professor_detail(request, professor_id, rev_sorting=rev_sorting)
        elif request.method == "POST" and "submit" in request.POST:
            LOGGER.debug(request.POST)
            review, message = add_review_from_details(request)
            return load_professor_detail(request, professor_id, review, message)
        else:
            LOGGER.error(request.POST)
            return error404(request, error="Invalid request")
    except Exception as e:
        LOGGER.exception(e)
        return error404(request, error=e)


def load_professor_detail(request: HttpRequest, professor_id: str, review: bool = None,
                          review_message: str = "",rev_sorting: str = "RevDateDesc") -> HttpResponse:
    try:
        professor = Professor.objects.get(pk=professor_id)
        classes = Class.objects.filter(professor_id=professor_id)
        courses_list = [cl.course for cl in classes]
        reviews_list = create_review_objects(classes, rev_sorting)
        reviews_avg = calculate_rating_avg(reviews_list)
        likes = []
        dislikes = []
        if request.user.id is not None:
            user = User.objects.get(username=request.user)
            likes = [vote.review.id for vote in Vote.objects.filter(user=user) if vote.vote == "L"]
            dislikes = [vote.review.id for vote in Vote.objects.filter(user=user) if vote.vote == "D"]

        paginator = Paginator(reviews_list, 10)
        page_number = request.GET.get('page')

        for rev in reviews_list:
            rev["like"] = len(Vote.objects.filter(review=rev['review_obj'], vote="L"))
            rev["dislike"] = len(Vote.objects.filter(review=rev['review_obj'], vote="D"))

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        if review is not None:
            context = {
                "professor": professor,
                "courses_list": courses_list,
                "reviews_list": reviews_list,
                "reviews_avg": reviews_avg,
                "review_saved": review,
                "review_message": review_message,
                "page_obj": page_obj,
                "likes": likes,
                "dislikes": dislikes,
                "sorting_reviews": rev_sorting,
            }
        else:
            context = {
                "professor": professor,
                "courses_list": courses_list,
                "reviews_list": reviews_list,
                "reviews_avg": reviews_avg,
                "page_obj": page_obj,
                "likes": likes,
                "dislikes": dislikes,
                "sorting_reviews": rev_sorting,
            }
        return render(request, "professors/detail.html", context)
    except Exception as e:
        return error404(request, error=e)


def like_review(request, review_id: str):
    return util_like_review(request=request, review_id=review_id)


def dislike_review(request, review_id: str):
    return util_dislike_review(request=request, review_id=review_id)
