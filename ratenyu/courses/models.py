import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from professors.models import Professor


class Course(models.Model):
    course_id = models.CharField(max_length=250, primary_key=True)
    course_title = models.CharField(max_length=250)
    course_subject_code = models.CharField(max_length=20, blank=True)
    catalog_number = models.CharField(max_length=20, blank=True)
    course_description = models.TextField(blank=True)


class Class(models.Model):
    class_id = models.CharField(max_length=250, primary_key=True)
    professor = models.ForeignKey(to=Professor, on_delete=models.CASCADE)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    class_type = models.CharField(max_length=250, blank=True)
    class_section = models.CharField(max_length=250, blank=True)
    term = models.CharField(max_length=250, blank=True)
    last_offered = models.CharField(max_length=250, blank=True)
    location = models.CharField(max_length=250, blank=True)
    enroll_capacity = models.PositiveIntegerField(blank=True)


class Review(models.Model):
    review_text = models.TextField(max_length=2200)
    rating = models.PositiveIntegerField(
        choices=((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"))
    )
    class_id = models.ForeignKey(to=Class, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.review_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Vote(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    review = models.ForeignKey(to=Review, on_delete=models.CASCADE)
    vote = models.CharField(max_length=1, choices=(("L", "L"), ("D", "D")))

class SavedCourse(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    professor_id = models.ForeignKey(to=Professor, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        unique_together = ('user_id', 'course_id')
