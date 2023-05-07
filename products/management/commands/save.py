from django.core.management import BaseCommand
from products.models import Products
import json

class Command(BaseCommand):
    @staticmethod
    def check_text(data: str) -> str:
        """
        Если текст содержит символ '\u2212' - заменить его на '-'.
        Двойную кавычку заменяем на двойную одинарную.

        """
        if isinstance(data, str):
            data.replace('"', "''")
            if data.find('\u2212') != -1:
                print("В тексте", data)
                print('сделана замена','\u2212', 'в позиции:', data.find('\u2212'))
            return data.replace('\u2212', '-')
        else:
            return data

    def handle(self, *args, **options):
        list_oject =[]
        text = "[\n"

        my_objects = Products.objects.order_by('id')

        for obj in my_objects:
            new_dict = {}
            text += "{\n"
            for key, value in obj.__dict__.items():
                if key != '_state':
                    text += f'"{key}":"{self.check_text(value)}",'
                    new_dict[key] = self.check_text(value)
            text += "\n},\n"
            list_oject.append(new_dict)
        text += "]\n"

        with open('save_data.json', 'w', encoding="utf-8") as file:
             file.write(text)  # сохранение данных файл