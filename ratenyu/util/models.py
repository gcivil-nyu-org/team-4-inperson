from django.db import models
from django.contrib.auth.models import User
from courses.models import Course, Class, Review
from professors.models import Professor

# Create your models here.


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
