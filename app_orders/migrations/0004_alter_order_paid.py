# Generated by Django 4.0.6 on 2022-08-29 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0003_alter_order_payment_method_delete_paymentmethod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='заказ оплачен'),
        ),
    ]
