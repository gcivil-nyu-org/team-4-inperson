"""ratenyu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("", include("search.urls")),
    path("admin/", admin.site.urls),
    path("professors/", include("professors.urls")),
    path("courses/", include("courses.urls")),
    path("error/", include("util.urls")),
    path("accounts/", include("allauth.urls")),
    path("logout_social/", LogoutView.as_view()),
    path("", include("users.urls")),
]

#404 url handler
handler404 = "util.views.page_not_found"

handler500 = "util.views.handler_500"