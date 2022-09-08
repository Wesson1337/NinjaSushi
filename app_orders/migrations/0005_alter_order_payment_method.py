# Generated by Django 4.1 on 2022-09-07 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0004_alter_order_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('card_c', 'Оплата картой курьеру'), ('cash', 'Оплата наличными курьеру')], default='card_o', max_length=6, verbose_name='способ оплаты'),
        ),
    ]