from django.core.files.images import ImageFile
from django.test import TestCase

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
            category_id=1
        )
        product1.image = ImageFile(open('app_cart/tests/img/tamago-maki.png', 'rb'))
        product1.save()

        product2 = Product.objects.create(
            name='Эби',
            amount=1,
            composition='Рис, креветка',
            weight=35,
            price=99,
            category_id=2,
        )
        product2.image = ImageFile(open('app_cart/tests/img/ebi.png', 'rb'))
        product2.save()

    def setUp(self) -> None:
        pass

    def test_product(self):
        product1 = Product.objects.get(id=1)
        self.assertEqual(product1.name, 'Тамаго-Маки')
