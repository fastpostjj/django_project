from django.db import models

NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class Blog(models.Model):
    """
    модель блоговой записи содержит следующие поля:

    заголовок
    slug (CharField)
    содержимое
    превью (изображение)
    дата создания
    признак публикации
    количество просмотров
    """
    '''
    title
    slug
    description
    preview
    is_active
    created_at
    is_published
    count_view
    '''
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(verbose_name='Превью', upload_to='blog/', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активная')
    created_at = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    is_published = models.BooleanField(verbose_name='Опубликована')
    count_view = models.IntegerField(verbose_name='Количество просмотров', **NULLABLE)



    def __str__(self):
        return f' Запись блога ({self.title}, {self.slug}, Опубликована: {self.is_active}, Дата создания:{self.created_at}, Количество просмотров:{self.count_view})'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('title', 'created_at',)