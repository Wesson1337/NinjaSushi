from django.db import models

from app_accounts.models import CustomUser
from app_cart.cart import Cart
from app_shop.models import Product

PAYMENT_METHODS = [
    ('card_c', 'Оплата картой курьеру'),
    ('cash', 'Оплата наличными курьеру')
]


class Order(models.Model):
    user = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='orders', verbose_name='Пользователь')
    name = models.CharField(max_length=50, verbose_name='имя')
    email = models.EmailField(verbose_name='электронная почта')
    phone_number = models.CharField(max_length=20, verbose_name='номер телефона')
    city = models.CharField(max_length=50, verbose_name='город')
    street = models.CharField(max_length=50, verbose_name='улица')
    house = models.PositiveIntegerField(verbose_name='дом')
    flat = models.PositiveIntegerField(verbose_name='квартира')
    floor = models.PositiveIntegerField(blank=True, verbose_name='этаж')
    intercom = models.CharField(max_length=20, blank=True, verbose_name='домофон')
    payment_method = models.CharField(max_length=6, choices=PAYMENT_METHODS, default='card_c',
                                      verbose_name='способ оплаты')
    created = models.DateTimeField(auto_now_add=True, verbose_name='время создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='время изменения')
    paid = models.BooleanField(default=False, verbose_name='заказ оплачен')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.id}'

    def get_total_cost(self) -> int:
        """Returns the total cost of the order"""
        return sum(item.get_cost() for item in self.items.all())
    get_total_cost.short_description = 'Итоговая стоимость'

    def get_full_address(self):
        """Returns full address in string format"""
        return f'г. {self.city}, ул. {self.street}, д. {self.house}, кв. {self.flat}'
    get_full_address.short_description = 'Адрес'

    def repeat_order(self, request):
        cart = Cart(request)
        cart.clear()
        for item in self.items.select_related('product').all():
            product_id = str(item.product.id)
            cart.cart[product_id] = {'quantity': item.quantity,
                                     'price': item.price}
        cart.save()


class OrderItem(models.Model):
    """Model for products in order"""

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='заказ')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='товар')
    price = models.PositiveIntegerField(verbose_name='цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='количество')

    def __str__(self):
        return f'Товар №{self.product.id} заказа №{self.order.id}'

    def get_cost(self) -> int:
        """Returns the cost of the item in the order"""
        return self.price * self.quantity
