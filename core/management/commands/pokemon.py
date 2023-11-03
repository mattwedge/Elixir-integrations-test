from django.core.management.base import BaseCommand, CommandError
import requests

from core.biz_rule import main


class Command(BaseCommand):
    help = "Ingests Random Pokemon Data"

    def handle(self, *args, **options):
        main()

        self.stdout.write(self.style.SUCCESS('Successfully run'))
