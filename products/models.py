from django.db import models

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
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(verbose_name='Превью', upload_to='products/', **NULLABLE)
    # category = models.CharField(max_length=150, verbose_name='Категория')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField(verbose_name='Цена', **NULLABLE)
    created_data = models.DateTimeField(verbose_name='Дата создания')
    last_changed_data = models.DateTimeField(verbose_name='Дата последнего изменения')
    is_active = models.BooleanField(default=True, verbose_name='активный')

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




