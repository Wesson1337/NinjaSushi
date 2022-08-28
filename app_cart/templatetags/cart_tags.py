from django import template
from app_cart.cart import Cart

register = template.Library()


@register.simple_tag
def cart_length(request) -> int:
    return len(Cart(request))
