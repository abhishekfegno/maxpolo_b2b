from django.core.management import BaseCommand

from apps.user.models import Dealer, Executive


class Command(BaseCommand):
    """ exec_dealer_map_file """

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, required=True)
        parser.add_argument('--exec', type=str, required=True)

    def handle(self, *args, **options):
        try:
            _exec = Executive.objects.get(pk=options.get('exec'))
        except Exception as e:
            print("Executive with this email doesnot exists.")
            return
        with open(options['file'], 'r') as fp:
            lines = [l.replace('\n', '') for l in fp.readlines()]
            if len(lines) is not Dealer.objects.all().filter(name__in=lines).count():
                print("Loading Data for ", _exec.name)
                print("Line Count : ", len(lines))
                print("DB Count : ", Dealer.objects.all().filter(name__in=lines).count())
                missing = []
                for dt in lines:
                    d = Dealer.objects.all().filter(name=dt).first()
                    if not d:
                        missing.append(dt)
                    else:
                        d.executive.remove(_exec)
                        d.executive.filter(executive=_exec).delete()
                        d.executive.add(_exec)
            print("Missing data : ", missing)
