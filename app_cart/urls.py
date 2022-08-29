from django.urls import path
from app_cart import views

app_name = 'app_cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart_view'),
    path('add/<int:product_id>/', views.cart_add_product, name='cart_add_product'),
    path('remove_unit/<int:product_id>/', views.cart_remove_unit_of_product, name='cart_remove_unit_of_product'),
    path('remove/<int:product_id>/', views.cart_remove_product, name='cart_remove_product'),
    path('clear/', views.cart_clear, name='cart_clear')
]
