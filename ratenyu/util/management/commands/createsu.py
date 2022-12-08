from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from decouple import config

class Command(BaseCommand):
    help = "Creates a superuser."

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(username="admin", password=config("ADMIN_PWD"))
        print("Superuser has been created.")
