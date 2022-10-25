from django.shortcuts import render

# Create your views here.


def error404(request, error=None):
    return render(request, "error.html", {"error": error})
