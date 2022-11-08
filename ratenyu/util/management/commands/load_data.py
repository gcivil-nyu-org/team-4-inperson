"""
This script generates data for the following tables
    Courses
    Classes
    Professors
    Reviews
"""

import csv
from django.utils import timezone
from pathlib import Path
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserDetails
from courses.models import Course, Class, Review
from professors.models import Professor

DATA_HOME = str(Path(__file__).resolve().parent.parent.parent)
COURSES = DATA_HOME + "/data/courses.csv"
PROFESSORS = DATA_HOME + "/data/professors.csv"
CLASSES = DATA_HOME + "/data/classes.csv"
USERS = DATA_HOME + "/data/users_dummy.csv"
REVIEWS = DATA_HOME + "/data/reviews_dummy.csv"


def create_new_course(row: "list[str]") -> None:
    new_course = Course(
        course_id=row[0],
        course_title=row[1],
        course_subject_code=row[2],
        catalog_number=row[3],
        course_description=row[4],
    )
    try:
        new_course.save()
    except Exception as e:
        print(e)


def create_new_professor(row: "list[str]") -> None:
    new_professor = Professor(
        professor_id=row[0], name=row[1], net_id=row[2], role=row[3]
    )
    try:
        new_professor.save()
    except Exception as e:
        print(e)


def create_new_class(row: "list[str]") -> None:
    new_class = Class(
        class_id=row[0],
        professor=Professor.objects.get(professor_id=row[1]),
        course=Course.objects.get(course_id=row[2]),
        class_type=row[3],
        class_section=row[4],
        term=row[5],
        last_offered=row[6],
        location=row[7],
        enroll_capacity=int(row[8]),
    )
    try:
        new_class.save()
    except Exception as e:
        print(e)


def create_new_user(row: "list[str]") -> None:
    if len(User.objects.filter(username=row[0])) > 0:
        return
    new_user = User(
        username=row[0],
        password=row[1],
        email=row[2]
    )
    try:
        new_user.save()
    except Exception as e:
        print(e)
    user_details = UserDetails(
        name=row[3],
        user=User.objects.get(username=row[0]),
        major=row[4],
        student_status=row[5],
    )
    try:
        user_details.save()
    except Exception as e:
        print(e)


def create_new_review(row: "list[str]") -> None:
    if len(Review.objects.filter(review_text=row[0])) > 0:
        return
    new_review = Review(
        review_text=row[0],
        rating=int(row[1]),
        class_id=Class.objects.get(class_id=row[2]),
        user=User.objects.get(id=row[3]),
        pub_date=timezone.now(),
    )
    try:
        new_review.save()
    except Exception as e:
        print(e)


def create_data(filename: str, model: str) -> None:
    with open(file=filename, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        if model == "course":
            for row in reader:
                create_new_course(row=row)
            print("Created course data.")
        elif model == "professor":
            for row in reader:
                create_new_professor(row=row)
            print("Created professor data.")
        elif model == "class":
            for row in reader:
                create_new_class(row=row)
            print("Created class data.")
        elif model == "user":
            for row in reader:
                create_new_user(row=row)
            print("Created dummy user data.")
        elif model == "review":
            next(reader)
            for row in reader:
                create_new_review(row=row)
            print("Created dummy review data.")


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_data(filename=COURSES, model="course")
        create_data(filename=PROFESSORS, model="professor")
        create_data(filename=CLASSES, model="class")
        create_data(filename=USERS, model="user")
        create_data(filename=REVIEWS, model="review")