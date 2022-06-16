from django.core.management import BaseCommand

from apps.executivetracking.models import Lead
from apps.user.models import Dealer, Executive


class Command(BaseCommand):

    def handle(self, *args, **options):
        Lead.objects.all().delete()
        Dealer.executive.through.objects.all().delete()

        for d in Dealer.objects.all():
            for e in Executive.objects.all():
                try:
                    d.executive.add(e)
                except Exception as e:
                    print(e)
