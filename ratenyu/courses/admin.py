from django.contrib import admin

from .models import Course, Class, Review, Vote, SavedCourse


admin.site.register(Course)
admin.site.register(Class)
admin.site.register(Review)
admin.site.register(Vote)
admin.site.register(SavedCourse)