from django.contrib.auth.models import AbstractUser
from django.db import models
# from products.models import NULLABLE
NULLABLE = {'null': True, 'blank': True}

# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users_auth/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=150, verbose_name='страна', **NULLABLE)
    # verification_kod = models.IntegerField(verbose_name="код подтверждения", **NULLABLE)
    # is_verify = models.BooleanField(verbose_name='прошел верификацию', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}" # , {'верифицирован' if self.is_verify else 'неверифицирован'}"

    # class Meta:
    #     verbose_name = 'Пользователь'
    #     verbose_name_plural = 'Пользователи'
    #     ordering = ('email',)

