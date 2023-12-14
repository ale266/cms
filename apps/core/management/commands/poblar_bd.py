import json
import uuid
from django.core.management import BaseCommand
from cmsapp.models import Category

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de ejemplo para la categoría'

    def handle(self, *args, **options):
        categories_data = [
            {
                "title": "Categoría 1",
                "slug": "categoria-1"
            },
            {
                "title": "Categoría 2",
                "slug": "categoria-2"
            },
            {
                "title": "Categoría 3",
                "slug": "categoria-3"
            },
            # Agrega más datos según sea necesario
        ]

        for category_data in categories_data:
            category = Category(**category_data)
            category.save()

            self.stdout.write(self.style.SUCCESS(f'Categoría "{category.title}" creada con éxito'))
