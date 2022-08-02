# Generated by Django 4.0.6 on 2022-08-01 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='img',
        ),
        migrations.AddField(
            model_name='product',
            name='composition',
            field=models.TextField(default=None, verbose_name='состав'),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default=2, upload_to='img/app_shop/product_images', verbose_name='фото'),
            preserve_default=False,
        ),
    ]
