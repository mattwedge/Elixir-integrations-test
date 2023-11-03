from django.core.management.base import BaseCommand, CommandError
import requests


class Command(BaseCommand):
    help = "Ingests Random MTG Data"

    def handle(self, *args, **options):
        # Using the mtg api (https://scryfall.com/) parse and prepare a json payload
        # and input it into the system using the models.

        self.stdout.write(self.style.SUCCESS('Successfully run'))
