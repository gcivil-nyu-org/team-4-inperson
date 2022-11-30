from django.shortcuts import render

# Create your views here.


def error404(request, error=""):
    return render(request, "error.html", {"error": error})

def page_not_found(request, exception):
    return error404(request,  f"We could not find the page you were looking for.")

def handler_500(request):
    return error404(request, f"We could not find the page you were looking for.")