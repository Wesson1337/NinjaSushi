from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from app_orders.tasks import order_created_email_task
from app_orders.models import OrderItem, Order
from app_shop.models import Product
from app_cart.cart import Cart
from django.views import View
from app_orders.forms import OrderForm


def cart_add_product(request, product_id: int) -> HttpResponseRedirect:
    """View to add product or unit of product to cart"""

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    url_came_from = request.META.get('HTTP_REFERER')
    return redirect(url_came_from) if url_came_from else redirect('app_shop:main_page')


def cart_remove_unit_of_product(request, product_id: int) -> HttpResponseRedirect:
    """View to remove unit of product from cart"""

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove_unit_of_product(product)
    url_came_from = request.META.get('HTTP_REFERER')
    return redirect(url_came_from) if url_came_from else redirect('app_shop:main_page')


def cart_remove_product(request, product_id: int) -> HttpResponseRedirect:
    """View to remove the entire product from cart"""

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove_product(product)
    url_came_from = request.META.get('HTTP_REFERER')
    return redirect(url_came_from) if url_came_from else redirect('app_shop:main_page')


def cart_clear(request) -> HttpResponseRedirect:
    """View to remove the entire cart from user session"""

    cart = Cart(request)
    cart.clear()
    url_came_from = request.META.get('HTTP_REFERER')
    return redirect(url_came_from) if url_came_from else redirect('app_shop:main_page')


class CartView(View):
    """View for rendering and post-processing cart_page.html"""
    def get(self, request) -> HttpResponse:
        cart = Cart(request)
        context = {'cart': cart}
        if request.user.is_authenticated:
            last_order = Order.objects.filter(user=request.user).last()
            context['last_order'] = last_order
        return render(request, 'app_cart/cart_page.html', context=context)

    def post(self, request) -> HttpResponseRedirect:
        cart = Cart(request)
        form = OrderForm(request.POST)
        if form.is_valid() and cart:
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            order_created_email_task.delay(order.id)
            return render(request, 'app_cart/cart_page_successful_order.html', context={'order_number': order.id})
        return redirect('app_cart:cart_view')
