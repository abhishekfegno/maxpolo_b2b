from django.core.management.base import BaseCommand

from apps.catalogue.models import Category


class Command(BaseCommand):
    help = "My shiny new management command."

    # def add_arguments(self, parser):
    #     parser.add_argument('sample', nargs='+')
    def create_category(self):
        roots = {
            'Size 2x2': {'Eco': '', 'Scheme': ['Scheme Series', 'Roto']},
            'Size 4x2': {'Eco': ['Glossy', 'Matt-Wood', 'Matt-Plain'],
                         'Scheme': ['Glossy', 'Matt-Plain', 'Matt-Punch', 'Carving']
                         },
            'Size 8x2': {'Scheme': ['Scheme Series']},
        }

        for root in roots:
            # root.items()
            # roots[root]
            # import pdb;
            # pdb.set_trace()
            rt = Category.objects.add_root(root)
            rt.add_child()

    def handle(self, *args, **options):
        self.create_category()
        raise NotImplementedError()

