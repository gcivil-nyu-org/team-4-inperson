from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


# Create your views here.
def professor_detail(request: HttpRequest, professor_id: str):
    return render(request, "professors/detail.html")
