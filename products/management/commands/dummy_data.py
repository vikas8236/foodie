from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Adds dummy products to the database'

    def handle(self, *args, **kwargs):
        if not Product.objects.exists():
            products = [
                {'name': 'Product 1', 'description': 'Description 1', 'price': 10.00},
                {'name': 'Product 2', 'description': 'Description 2', 'price': 20.00},
            ]

            for product_data in products:
                Product.objects.create(**product_data)

            self.stdout.write(self.style.SUCCESS('Successfully added dummy products'))
        else:
            self.stdout.write(self.style.NOTICE('Dummy products already exist'))
