from django.contrib import admin

# Register your models here.


from util.models import Vote, SavedCourse

admin.site.register(Vote)
admin.site.register(SavedCourse)