import tempfile
from django.test import TestCase, Client
from django.urls import reverse

from app_cart.cart import Cart
from app_shop.models import Product, Category


class CartTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        category1 = Category.objects.create(name='Роллы')
        category1.save()

        category2 = Category.objects.create(name='Суши')
        category2.save()

        product1 = Product.objects.create(
            name='Тамаго-Маки',
            amount=8,
            composition='Рис, огурец, лосось',
            weight=120,
            price=200,
            category_id=1,
            image=tempfile.NamedTemporaryFile(suffix='.png').name
        )
        product1.save()

        product2 = Product.objects.create(
            name='Эби',
            amount=1,
            composition='Рис, креветка',
            weight=35,
            price=99,
            category_id=2,
            image=tempfile.NamedTemporaryFile(suffix='.png').name
        )
        product2.save()

        cls.product1 = product1
        cls.product2 = product2

    def setUp(self) -> None:
        self.client = Client()
        self.get_response = self.client.get(reverse('app_shop:main_page'))
        self.get_request = self.get_response.wsgi_request
        self.cart = Cart(self.get_request)
        self.cart.add(product=self.product1)
        self.cart.add(product=self.product1)
        self.cart.add(product=self.product2)

    def test_cart_add(self):
        cart, get_request = self.cart, self.get_request
        cart.save()
        self.assertEqual(get_request.session['cart'], {
            '1': {'quantity': 2, 'price': 200},
            '2': {'quantity': 1, 'price': 99}
        })

    def test_cart_remove_unit_of_product(self):
        cart, get_request, product1, product2 = self.cart, self.get_request, self.product1, self.product2
        cart.remove_unit_of_product(product=product1)
        cart.remove_unit_of_product(product=product2)
        self.assertEqual(get_request.session['cart'], {
            '1': {'quantity': 1, 'price': 200}
        })

    def test_cart_iterations(self):
        cart, get_request, product1 = self.cart, self.get_request, self.product1
        for item in cart:
            self.assertTrue(isinstance(item['product'], Product))
            product = item['product']
            if product == product1:
                self.assertEqual(item, {
                    'product': product,
                    'quantity': 2,
                    'price': 200,
                    'total_price': 400
                })
            else:
                self.assertEqual(item, {
                    'product': product,
                    'quantity': 1,
                    'price': 99,
                    'total_price': 99
                })

    def test_cart_remove_product(self):
        cart, get_request, product1 = self.cart, self.get_request, self.product1
        cart.remove_product(product1)
        self.assertEqual(get_request.session['cart'], {
            '2': {'quantity': 1, 'price': 99}
        })

    def test_cart_get_total_price(self):
        self.assertEqual(self.cart.get_total_price(), 499)

    def test_cart_clear(self):
        cart, get_request = self.cart, self.get_request
        cart.clear()
        self.assertEqual(cart.cart, {})
        self.assertEqual(get_request.session.get('cart'), None)
