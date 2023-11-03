from django.core.management.base import BaseCommand, CommandError
import requests


class Command(BaseCommand):
    help = "Ingests Random Pokemon Data"

    def handle(self, *args, **options):
        # Using the pokemon api (https://pokemontcg.io/) parse and prepare a json payload
        # and input it into the system using the models.

        self.stdout.write(self.style.SUCCESS('Successfully run'))
