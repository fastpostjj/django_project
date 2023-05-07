from django.core.management import BaseCommand
from products.models import Products
import json

class Command(BaseCommand):
    @staticmethod
    def check_text(data) -> str:
        """
        Если текст содержит символ '\u2212' - заменить его на '-'.
        Двойную кавычку заменяем на двойную одинарную.
        Другие типы данных игнорируем.

        """
        if isinstance(data, str):
            if data.find('"') != -1:
                print("В тексте", data)
                print('сделана замена символа ', '"', 'в позиции:', data.find('"'))
                data=data.replace('"', "''")
            if data.find('\u2212') != -1:
                print("В тексте", data)
                print('сделана замена символа ','\u2212', 'в позиции:', data.find('\u2212'))
                data = data.replace('\u2212', '-')

        return data

    def handle(self, *args, **options):
        text = "[\n"

        my_objects = Products.objects.order_by('id')

        for obj in my_objects:
            new_dict = {}
            text += "{\n"
            for key, value in obj.__dict__.items():
                if key != '_state':
                    text += f'"{key}":"{self.check_text(value)}",\n'
                    new_dict[key] = self.check_text(value)
            text = text[:-2] + "\n},\n"
        text = text[:-2] + "\n]\n"

        with open('save_data.json', 'w', encoding="utf-8") as file:
             file.write(text)  # сохранение данных файл

