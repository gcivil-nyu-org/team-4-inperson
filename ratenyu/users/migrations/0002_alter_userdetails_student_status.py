# Generated by Django 4.1.2 on 2022-11-29 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userdetails",
            name="student_status",
            field=models.CharField(
                choices=[
                    ("Freshman", "Freshman"),
                    ("Sophomore", "Sophomore"),
                    ("Junior", "Junior"),
                    ("Senior", "Senior"),
                    ("Master1", "Master1"),
                    ("Master2", "Master2"),
                    ("PHD", "PHD"),
                ],
                max_length=30,
            ),
        ),
    ]
