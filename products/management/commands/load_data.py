from django.core.management import BaseCommand
from products.models import Products, Category
import json
from json import JSONDecodeError

class Command(BaseCommand):

    @staticmethod
    def delete_all():
        """
        Удаляем все записи в базе данных
        """
        list_category = Category.objects.all()
        list_products = Products.objects.all()
        for item in list_products:
            item.delete()

        for item in list_category:
            item.delete()


    @staticmethod
    def get_product_from_dict(item:dict) -> Products:
        """Получаем данные о продуктах из файла"""
        if isinstance(item, dict):
            id = 0
            name = ""
            description = ""
            image = ""
            price = 0
            created_data = None
            last_changed_data = None

            if 'category_id' in item:
                category = Category.objects.get(pk=int(item['category_id']))
                if 'id' in item:
                    id = int(item['id'])
                if 'name' in item:
                    name = item['name']
                if 'description' in item:
                    description = item['description']
                if 'image' in item:
                    image = item['image']
                    if 'price' in item:
                        price = float(item['price'])
                    if 'created_data' in item:
                        created_data = item['created_data']
                    if 'last_changed_data' in item:
                        last_changed_data = item['last_changed_data']
                    product = Products.objects.create(
                        id=id,
                        name=name,
                        description=description,
                        image=image,
                        category=category,
                        price=price,
                        created_data=created_data,
                        last_changed_data=last_changed_data)
                    return product
            else:
                print("Отсутствует категория товара в базе данных для продукта ", name)
        else:
            raise KeyError("Ожидается словарь: ", item)

    @staticmethod
    def get_category_from_dict(item: dict) -> Category:
        """Получаем данные о категориях из файла"""

        if isinstance(item, dict):
            id = 0
            name = ""
            description = ""

            if 'id' in item:
                id = int(item['id'])
            if 'name' in item:
                name = item['name']
            if 'description' in item:
                description = item['description']
            category = Category.objects.create(
                id=id,
                name=name,
                description=description,
                )
            return category
        else:
            raise KeyError("Ожидается словарь: ", item)

    def handle(self, *args, **options):
        # Удаляем все записи
        self.delete_all()

       # Загружаем категории
        with open('save_category.json', 'r', encoding="utf-8") as file:
            list_json = json.load(file)
            if isinstance(list_json, list):
                for item in list_json:
                    category = self.get_category_from_dict(item)
                    if category:
                        category.save()
            elif isinstance(list_json, dict):
                category = self.get_category_from_dict(list_json)
                if category:
                    category.save()

        # Загружаем продукты
        with open('save_data.json', 'r', encoding="utf-8") as file:
            list_json = json.load(file)

            if isinstance(list_json, list):
                for item in list_json:
                    product = self.get_product_from_dict(item)
                    if product:
                        product.save()
            elif isinstance(list_json, dict):
                product = self.get_product_from_dict(list_json)
                if product:
                 product.save()


