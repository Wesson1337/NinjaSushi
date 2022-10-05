from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="номер телефона")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='день рождения')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
