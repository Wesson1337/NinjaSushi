import tempfile

from django.test import TestCase, Client
from django.urls import reverse

from app_orders.models import Order, OrderItem
from app_shop.models import Product, Category


class TestOrderModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        order = Order.objects.create(
            name='test',
            email='test@mail.ru',
            phone_number='test',
            city='test',
            street='test',
            house=6,
            flat=3,
            floor=3,
            intercom=3,
            payment_method='card_c'
        )
        order.save()

        category = Category.objects.create(name='Роллы')
        category.save()

        product = Product.objects.create(
            name='Тамаго-Маки',
            amount=8,
            composition='Рис, огурец, лосось',
            weight=120,
            price=200,
            category=category,
            image=tempfile.NamedTemporaryFile(suffix='.png').name
        )
        product.save()

        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            price=product.price,
            quantity=2
        )
        order_item.save()

        cls.order = order
        cls.order_item = order_item
        cls.product = product

    def test_order_string(self):
        order = self.order
        self.assertIsInstance(str(order), str)

    def test_order_get_total_cost(self):
        order = self.order
        self.assertEqual(order.get_total_cost(), 400)

    def test_order_get_full_address(self):
        order = self.order
        self.assertIsInstance(order.get_full_address(), str)

    def test_order_repeat_order(self):
        client = Client()
        order = self.order
        response = client.get(reverse('app_shop:main_page'))
        request = response.wsgi_request
        order.repeat_order(request)
        self.assertEqual(request.session['cart'], {
            str(self.product.id): {
                'quantity': 2,
                'price': 200
            }
        })

    def test_order_item_string(self):
        order_item = self.order_item
        self.assertIsInstance(str(order_item), str)
