from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='название')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')
    amount = models.PositiveIntegerField(verbose_name='количество (шт.)')
    composition = models.TextField(default=None, blank=True, verbose_name='состав')
    weight = models.PositiveIntegerField(verbose_name='вес (гр.)')
    price = models.PositiveIntegerField(verbose_name='цена (₽)')
    image = models.ImageField(upload_to='img/app_shop/product_images', verbose_name='фото')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return f"{self.name}"
