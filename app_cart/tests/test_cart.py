import tempfile

from django.test import TestCase, Client
from django.urls import reverse

from app_accounts.models import CustomUser
from app_cart.cart import Cart
from app_orders.models import Order
from app_shop.models import Product, Category


class CartTest(TestCase):

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
            category=category2,
            image=tempfile.NamedTemporaryFile(suffix='.png').name
        )
        product1.save()

        product2 = Product.objects.create(
            name='Эби',
            amount=1,
            composition='Рис, креветка',
            weight=35,
            price=99,
            category=category2,
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
        get_request = self.get_request
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
            self.assertIsInstance(item['product'], Product)
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

    def test_cart_add_product_view(self):
        response = self.client.get(reverse('app_cart:cart_add_product', args=[self.product1.id]))
        self.assertRedirects(response, reverse('app_shop:main_page'), status_code=302,
                             target_status_code=200)

    def test_cart_remove_unit_of_product_view(self):
        response = self.client.get(reverse('app_cart:cart_remove_unit_of_product', args=[self.product1.id]))
        self.assertRedirects(response, reverse('app_shop:main_page'), status_code=302,
                             target_status_code=200)

    def test_cart_remove_product_view(self):
        response = self.client.get(reverse('app_cart:cart_remove_product', args=[self.product1.id]))
        self.assertRedirects(response, reverse('app_shop:main_page'), status_code=302,
                             target_status_code=200)

    def test_cart_clear_view(self):
        response = self.client.get(reverse('app_cart:cart_clear'))
        self.assertRedirects(response, reverse('app_shop:main_page'), status_code=302,
                             target_status_code=200)

    def test_cart_get_view(self):
        user = CustomUser.objects.create_user(username='user_test', password='Testu123ser', first_name='test_user',
                                              date_of_birth='2022-09-30', phone_number='fds')
        user.save()
        self.client.login(username='user_test', password='Testu123ser')
        order = Order.objects.create(user=user, name='test', email='test@mail.ru', city='test',
                                     street='test', flat=6, house=5, floor=3)
        order.save()
        response = self.client.get(reverse('app_cart:cart_view'))
        self.assertEqual(response.context['last_order'], order)
        self.assertIsInstance(response.context['cart'], Cart)
        self.assertEqual(response.status_code, 200)

    def test_cart_post_view(self):
        session = self.client.session
        session['cart'] = self.get_request.session['cart']
        session.save()
        user = CustomUser.objects.create_user(username='user_test', password='Testu123ser', first_name='test_user',
                                              date_of_birth='2022-09-30', phone_number='fds')
        user.save()
        self.client.login(username='user_test', password='Testu123ser')
        response = self.client.post(reverse('app_cart:cart_view'), data={'name': 'test',
                                                                         'email': 'test@mail.ru',
                                                                         'phone_number': 'test',
                                                                         'city': 'test',
                                                                         'street': 'test',
                                                                         'house': 5,
                                                                         'flat': 3,
                                                                         'floor': 2,
                                                                         'intercom': 'fsdaffd',
                                                                         'payment_method': 'card_c'
                                                                         })
        self.assertEqual(response.status_code, 200)
        order = Order.objects.last()
        self.assertEqual(order.user, user)
        for item in order.items.all():
            if item.product.id == 1:
                self.assertEqual(item.price, 200)
                self.assertEqual(item.quantity, 2)
            else:
                self.assertEqual(item.price, 99)
                self.assertEqual(item.quantity, 1)

    def test_cart_post_view_incorrect_data(self):
        session = self.client.session
        session['cart'] = self.get_request.session['cart']
        session.save()
        response = self.client.post(reverse('app_cart:cart_view'), data={'name': 'test'})
        self.assertRedirects(response, reverse('app_cart:cart_view'))
