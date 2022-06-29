from django.core.management.base import BaseCommand

from apps.catalogue.models import Category


class Command(BaseCommand):
    help = "My shiny new management command."

    # def add_arguments(self, parser):
    #     parser.add_argument('sample', nargs='+')
    def create_category(self):
        print("Deleting Categories...........")
        Category.objects.all().delete()

        roots = {
            'Size 2x2': {'Eco': '', 'Scheme': ['Scheme Series', 'Roto']},
            'Size 4x2': {'Eco': ['Glossy', 'Matt-Wood', 'Matt-Plain'],
                         'Scheme': ['Glossy', 'Matt-Plain', 'Matt-Punch', 'Carving']
                         },
            'Size 8x2': {'Scheme': ['Scheme Series']},
        }

        for root in roots:
            rt = Category.add_root(name=root)
            for i in roots[root]:
                child = rt.add_child(name=i)
                for j in roots[root][i]:
                    child.add_child(name=j)

    def handle(self, *args, **options):
        self.create_category()
        # raise NotImplementedError()
