from django.test import TestCase, Client
from django.urls import reverse

from app_accounts.models import CustomUser
from app_orders.models import Order


class AccountsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        user = CustomUser.objects.create_user(username='user_test', password='Testu123ser', first_name='test_user',
                                              date_of_birth='2022-09-30', phone_number='fds')
        user.save()

        order = Order.objects.create(
            user=user,
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

        cls.user = user
        cls.order = order

    def test_personal_account_view_user_not_authenticated(self):
        client = self.client
        response = client.get(reverse('app_accounts:personal_account'))
        self.assertRedirects(response, reverse('app_accounts:login'))

    def test_personal_account_view_user_authenticated(self):
        client = self.client
        client.login(username='user_test', password='Testu123ser')
        response = client.get(reverse('app_accounts:personal_account'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['orders'][0], self.order)

    def test_registration_view_get(self):
        client = self.client
        response = client.get(reverse('app_accounts:registration'))
        self.assertEqual(response.status_code, 200)

    def test_registration_view_post(self):
        client = self.client
        response = client.post(reverse('app_accounts:registration'), {'username': 'user_test2',
                                                                      'email': 'test@mail.ru',
                                                                      'password1': 'Hgfdsa123123',
                                                                      'password2': 'Hgfdsa123123',
                                                                      'first_name': 'test_user',
                                                                      'date_of_birth': '2022-09-30',
                                                                      'phone_number': 'fds'})
        self.assertRedirects(response, reverse('app_accounts:personal_account'))
        new_user = CustomUser.objects.get(username='user_test2')
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user, new_user)

    def test_logout_view(self):
        client = self.client
        client.login(username='user_test', password='Testu123ser')
        response = client.get(reverse('app_shop:main_page'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        response = client.get(reverse('app_accounts:logout'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
