from django.core.management import BaseCommand

from main.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        category_list = [
            {'name': 'Мясо', 'description': 'Свежее мясо'},
            {'name': 'Рыба', 'description': 'Свежая рыба'},
            {'name': 'Бакалея', 'description': 'Всегда свежее'},
            {'name': 'Молочные продукты', 'description': 'Отборное молоко'},
            {'name': 'Крупы', 'description': 'Отборные крупы'},
            {'name': 'Напитки', 'description': 'Холодные напитки'},
            {'name': 'Ягоды', 'description': 'Свежие ягоды'},
        ]
        category_for_create = []
        for category_item in category_list:
            category_for_create.append(
                Category(**category_item)
            )
        Category.objects.bulk_create(category_for_create)

