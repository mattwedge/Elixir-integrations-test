from django.core.management.base import BaseCommand, CommandError
import requests


class Command(BaseCommand):
    help = "Ingests Random Marvel Data"

    def handle(self, *args, **options):
        # Using the marvel api (https://developer.marvel.com/) parse and prepare a json payload
        # and input it into the system using the models.

        self.stdout.write(self.style.SUCCESS('Successfully run'))
