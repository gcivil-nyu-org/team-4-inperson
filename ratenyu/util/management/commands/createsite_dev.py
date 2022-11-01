"""
This script creates the necessary Admin sites for OAuth/OpenID
"""

from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    def handle(self, *args, **options):
        site_name = "ratenyu-dev.eba-apngxcqy.us-east-1.elasticbeanstalk.com"
        if not Site.objects.filter(domain=site_name).exists():
            Site.objects.create(domain=site_name, name=site_name)
        print(f"Site {site_name} has been created.")
