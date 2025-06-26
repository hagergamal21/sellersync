from django.core.management.base import BaseCommand
from demand_forecasting.models import SubCategory, SemanticLabel

class Command(BaseCommand):
    help = 'Populate SubCategory and SemanticLabel tables'

    def handle(self, *args, **kwargs):
        # Semantic Labels
        semantic_labels = ['Kids', 'Men', 'Unisex', 'Women']
        for label in semantic_labels:
            SemanticLabel.objects.get_or_create(label=label)
            self.stdout.write(self.style.SUCCESS(f'Added SemanticLabel: {label}'))

        # SubCategories (limited to a few for testing, add more as needed)
        subcategories = [
            'Accessories', 'Jeans', 'Dresses', 'Bags', 'Shoes', 'Tops'
        ]
        for name in subcategories:
            SubCategory.objects.get_or_create(name=name)
            self.stdout.write(self.style.SUCCESS(f'Added SubCategory: {name}'))