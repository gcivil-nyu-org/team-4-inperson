from users.models import User, UserDetails
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Creates test users"

    def handle(self, *args, **options):
        if not User.objects.filter(username="testuser1").exists():
            user = User.objects.create(username="testuser1", email="testuser1@nyu.edu")
            user.set_password("testuser1")
            user.save()
            UserDetails.objects.create(user=User.objects.get(username="testuser1"), name="Test User 1", major="Computer Science", student_status="Master2")
        if not User.objects.filter(username="testuser2").exists():
            user = User.objects.create(username="testuser2", email="testuser2@nyu.edu")
            user.set_password("testuser2")
            user.save()
            UserDetails.objects.create(user=User.objects.get(username="testuser2"), name="Test User 2", major="Computer Science", student_status="Master2")
        if not User.objects.filter(username="testuser3").exists():
            user = User.objects.create(username="testuser3", email="testuser3@nyu.edu")
            user.set_password("testuser3")
            user.save()
            UserDetails.objects.create(user=User.objects.get(username="testuser3"), name="Test User 3", major="Computer Science", student_status="Master2")
        if not User.objects.filter(username="testuser4").exists():
            user = User.objects.create(username="testuser4", email="testuser4@nyu.edu")
            user.set_password("testuser4")
            user.save()
            UserDetails.objects.create(user=User.objects.get(username="testuser4"), name="Test User 4", major="Computer Science", student_status="Master2")
        if not User.objects.filter(username="testuser5").exists():
            user = User.objects.create(username="testuser5", email="testuser5@nyu.edu")
            user.set_password("testuser5")
            user.save()
            UserDetails.objects.create(user=User.objects.get(username="testuser5"), name="Test User 5", major="Computer Science", student_status="Master2")
        if not User.objects.filter(username="testuser6").exists():
            user = User.objects.create(username="testuser6", email="testuser6@nyu.edu")
            user.set_password("testuser6")
            user.save()
            UserDetails.objects.create(user=User.objects.get(username="testuser6"), name="Test User 6", major="Computer Science", student_status="Master2")
        if not User.objects.filter(username="testuser7").exists():
            user = User.objects.create(username="testuser7", email="testuser7@nyu.edu")
            user.set_password("testuser7")
            user.save()
            UserDetails.objects.create(user=User.objects.get(username="testuser7"), name="Test User 7", student_status="Master2")
        
            
