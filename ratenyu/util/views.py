from django.shortcuts import render

# Create your views here.


def error404(request, error=""):
    return render(request, "error.html", {"error": error})

def page_not_found(request, exception):
    return error404(request, "error.html", {"error": "We could not find the page you were looking for."})