from csv import reader

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
                'recipes/data/ingredients.csv',
                encoding='UTF-8'
        ) as f:
            for row in reader(f):
                name, measurement_unit = row
                if len(row) == 2:
                    Ingredient.objects.get_or_create(
                        name=name, measurement_unit=measurement_unit,
                    )
