import itertools

from django.db import models
# from django.template.defaultfilters import slugify
from django.utils.text import slugify

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
    slug = models.CharField(max_length=150, unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(verbose_name='Превью', upload_to='blog/', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активная')
    created_at = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    is_published = models.BooleanField(verbose_name='Опубликована')
    count_view = models.IntegerField(verbose_name='Количество просмотров', default=0)



    def __str__(self):
        return f' Запись блога ({self.title}, Дата создания:{self.created_at}, Количество просмотров:{self.count_view})'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        return super().save(*args, **kwargs)

    def _generate_slug(self):
        slug_candidate = slugify(self.title, allow_unicode=False)
        if not slug_candidate:
            slug_candidate = "s"
        for i in itertools.count(1):
            if not Blog.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_candidate, i)
        self.slug = slug_candidate
        return self.slug


    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('title', 'created_at',)