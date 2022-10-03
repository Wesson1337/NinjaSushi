import tempfile

from django.test import TestCase, Client
from django.urls import reverse

from app_newsletter.models import NewsletterEmail
from app_shop.models import Category, Product


class ShopViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        category1 = Category.objects.create(name='Роллы')
        category1.save()

        category2 = Category.objects.create(name='Суши')
        category2.save()

        cls.category1 = category1
        cls.category2 = category2

        product1 = Product.objects.create(
            name='Тамаго-Маки',
            amount=8,
            composition='Рис, огурец, лосось',
            weight=120,
            price=200,
            category=category1,
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

    def test_get_main_page(self):
        client = self.client
        response = client.get(reverse('app_shop:main_page'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['products'][0], self.product1)
        self.assertEqual(response.context['products'][1], self.product2)
        self.assertEqual(response.context['categories'][0], self.category1)
        self.assertEqual(response.context['categories'][1], self.category2)

    def test_post_main_page_email_exists(self):
        client = self.client
        NewsletterEmail.objects.create(email='test@mail.ru')
        response = client.post(reverse('app_shop:main_page'), {'email': 'test@mail.ru'})
        self.assertRedirects(response, reverse('app_shop:main_page'), status_code=302,
                             target_status_code=200)
        email_counter = NewsletterEmail.objects.filter(email='test@mail.ru').count()
        self.assertEqual(email_counter, 1)

    def test_post_main_page_email_not_exists(self):
        client = self.client
        response = client.post(reverse('app_shop:main_page'), {'email': 'test@mail.ru'})
        self.assertRedirects(response, reverse('app_shop:main_page'), status_code=302,
                             target_status_code=200)
        email = NewsletterEmail.objects.last()
        self.assertEqual(email.email, 'test@mail.ru')

    def test_get_main_page_detail(self):
        client = self.client
        response = client.get(reverse('app_shop:main_page_detail', args=[self.category1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['categories'][0], self.category1)
        self.assertEqual(response.context['category'], self.category1)
        self.assertEqual(response.context['products'][0], self.product1)



