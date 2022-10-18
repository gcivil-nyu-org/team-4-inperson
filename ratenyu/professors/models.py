from django.db import models


class Professor(models.Model):
    professor_id = models.CharField(max_length=250, primary_key=True)
    name = models.CharField(max_length=250)
    net_id = models.CharField(max_length=250)
    role = models.CharField(max_length=250)
