from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

from app_orders.models import OrderItem
from app_shop.models import Product
from app_cart.cart import Cart
from django.views import View
from app_orders.forms import OrderForm


def cart_add_product(request, product_id: int) -> HttpResponseRedirect:
    """View to add product or unit of product to cart"""

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_remove_unit_of_product(request, product_id: int) -> HttpResponseRedirect:
    """View to remove unit of product from cart"""

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove_unit_of_product(product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_remove_product(request, product_id: int) -> HttpResponseRedirect:
    """View to remove the entire product from cart"""

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove_product(product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_clear(request) -> HttpResponseRedirect:
    """View to remove the entire cart from user session"""

    cart = Cart(request)
    cart.clear()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CartView(View):

    def get(self, request) -> HttpResponse:
        cart = Cart(request)
        form = OrderForm
        return render(request, 'app_cart/cart_page.html', context={'cart': cart, 'form': form})

    def post(self, request):
        cart = Cart(request)
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return HttpResponseRedirect('/')

