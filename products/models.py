from django.core.exceptions import ValidationError
from django.db import models
from user_auth.models import User

NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class Category(models.Model):
    """
    Наименование
    Описание
    """
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='активный')
    # created_at = models.DateTimeField(verbose_name='Дата создания', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name', )

class Products(models.Model):
    """
    Наименование
    Описание
    Изображение (превью)
    Категория
    Цена за покупку
    Дата создания
    Дата последнего изменения
    """
    user = User.objects.filter(pk=2)
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(verbose_name='Превью', upload_to='products/', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField(verbose_name='Цена', **NULLABLE)
    created_data = models.DateTimeField(verbose_name='Дата создания')
    last_changed_data = models.DateTimeField(verbose_name='Дата последнего изменения')
    is_active = models.BooleanField(default=True, verbose_name='активный')
    user = models.ForeignKey(User, verbose_name='пользователь-автор', default=None, on_delete=models.SET_NULL, **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name='опубликован')

    def __str__(self):
        # return f'{self.id} {self.name}, {self.category}, {self.price}'
        return f'{self.name}'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('name', 'price')
        permissions = {
            ("set_published_status", "can published product"),
            ("set_description_status", "can change description product"),
            ("set_category_status", "can change category product")

        }

class Version(models.Model):
    """
    модель «Версия» содержит следующие поля:

    продукт,
    номер версии,
    название версии,
    признак текущей версии.
    При наличии активной версии реализовать вывод в список продуктов информации об активной версии.
    product
    version_number
    version_title
    is_active

    """
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="Название продукта")
    version_number = models.IntegerField(verbose_name="Номер версии", **NULLABLE)
    version_title = models.CharField(max_length=150, verbose_name="Наименование версии", **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='активный')

    def __str__(self):
        return f"Версия № {self.version_number}, {self.version_title}"

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


    def save(self, *args, **kwargs):
        # проверяем, есть ли уже активная версия для этого продукта
        if self.is_active and Version.objects.filter(product=self.product, is_active=True).exclude(pk=self.pk).exists():
            raise ValidationError('Нельзя добавить более одной активной версии для данного продукта.')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
        ordering = ('version_number',)






