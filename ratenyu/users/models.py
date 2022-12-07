from django.db import models
from django.contrib.auth.models import User


class UserDetails(models.Model):
    STATUS_CHOICES = [
        ("Freshman", "Freshman"),
        ("Sophomore", "Sophomore"),
        ("Junior", "Junior"),
        ("Senior", "Senior"),
        ("Master1", "Master1"),
        ("Master2", "Master2"),
        ("PHD", "PHD"),
    ]

    LIST_OF_MAJORS = [
        ("Applied Physics","Applied Physics"),
        ("Nuclear Sciences and Engineering","Nuclear Sciences and Engineering"),
        ("Physics and Mathematics","Physics and Mathematics"),
        ("Bioinformatics","Bioinformatics"),
        ("Biomolecular Science","Biomolecular Science"),
        ("Biotechnology","Biotechnology"),
        ("Biotechnology and Entrepreneurship","Biotechnology and Entrepreneurship"),
        ("Chemical and Biomolecular Engineering","Chemical and Biomolecular Engineering"),
        ("Chemical Engineering (Guided Studies & MS Thesis Option)","Chemical Engineering (Guided Studies & MS Thesis Option)"),
        ("Chemistry","Chemistry"),
        ("Civil Engineering","Civil Engineering"),
        ("Construction Management","Construction Management"),
        ("Transportation Management","Transportation Management"),
        ("Transportation Planning and Engineering","Transportation Planning and Engineering"),
        ("Computer Science","Computer Science"),
        ("Cybersecurity","Cybersecurity"),
        ("Computer Engineering","Computer Engineering"),
        ("Electrical Engineering","Electrical Engineering"),
        ("Financial Engineering","Financial Engineering"),
        ("Mathematics","Mathematics"),
        ("Aerospace Engineering","Aerospace Engineering"),
        ("Mechanical Engineering","Mechanical Engineering"),
        ("Integrated Digital Media","Integrated Digital Media"),
        ("Science and Technology Studies","Science and Technology Studies"),
        ("Sustainable Urban Environments","Sustainable Urban Environments"),
        ("Management","Management"),
        ("Management of Technology","Management of Technology"),
        ("Others (not in list)","Others (not in list)"),
    ]
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(
        max_length=100,
        choices=LIST_OF_MAJORS,
    ) 
    student_status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
    )
