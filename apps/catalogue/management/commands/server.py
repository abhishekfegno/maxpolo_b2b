from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self):
        pass
