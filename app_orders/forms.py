from django import forms
from app_orders.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'phone_number', 'city', 'street', 'house', 'flat', 'floor', 'intercom',
                  'payment_method']
