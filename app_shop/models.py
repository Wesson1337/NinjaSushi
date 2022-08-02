from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')
    amount = models.PositiveIntegerField(verbose_name='количество')
    composition = models.TextField(default=None, verbose_name='состав')
    weight = models.PositiveIntegerField(verbose_name='вес')
    price = models.PositiveIntegerField(verbose_name='цена')
    image = models.ImageField(upload_to='img/app_shop/product_images', verbose_name='фото')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return f"{self.name}"
