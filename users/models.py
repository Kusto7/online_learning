from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=40, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='город', **NULLABLE)
    register_uuid = models.CharField(max_length=50, **NULLABLE)
    moderator = models.BooleanField(default=False, verbose_name="модератор")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

