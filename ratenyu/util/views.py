from django.shortcuts import render


def error404(request, error=""):
    return render(request, "error.html", {"error": error})


def util_like_review(request, review_id: str):
    LOGGER.debug(f"like_review: {review_id}")
    response = HttpResponse()
    try:
        if request.method == 'POST':
            review = Review.objects.get(pk=review_id)
            user = User.objects.get(username=request.user.username)
            try:
                vote = Vote.objects.get(review=review, user=user)
                if vote.vote == 'L':
                    vote.delete()
                    return response
                else:
                    vote.vote = 'L'
                    vote.save()
                    return response
            except Vote.DoesNotExist:
                vote = Vote(review=review, user=user, vote="L")
                vote.save()
                return response
    except Exception as e:
        LOGGER.exception(f"Could not like review, encountered error: {e}")
        return HttpResponse(status=500)


def util_dislike_review(request, review_id: str):
    LOGGER.debug(f"dislike_review: {review_id}")
    response = HttpResponse()
    try:
        if request.method == 'POST':
            review = Review.objects.get(pk=review_id)
            user = User.objects.get(username=request.user.username)
            try:
                vote = Vote.objects.get(review=review, user=user)
                if vote.vote == 'D':
                    vote.delete()
                    return response
                else:
                    vote.vote = 'D'
                    vote.save()
                    return response
            except Vote.DoesNotExist:
                vote = Vote(review=review, user=user, vote="D")
                vote.save()
                return response
    except Exception as e:
        LOGGER.exception(f"Could not dislike review, encountered error: {e}")
        return HttpResponse(status=500)


def page_not_found(request, exception):
    return error404(request,  f"We could not find the page you were looking for.")


def handler_500(request):
    return error404(request, f"We could not find the page you were looking for.")
