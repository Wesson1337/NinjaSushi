from django.conf import settings
from app_shop.models import Product


class Cart:
    """Class to manage cart in user session."""

    def __init__(self, request):
        """Initialize cart."""

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product: Product) -> None:
        """Add product or one unit of product to cart."""

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        self.cart[product_id]['quantity'] += 1
        self.save()

    def remove_unit_of_product(self, product: Product) -> None:
        """Remove one unit of product from cart."""

        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]['quantity'] >= 1:
                self.cart[product_id]['quantity'] -= 1
            else:
                del self.cart[product_id]
            self.save()

    def remove_product(self, product: Product) -> None:
        """Remove the entire product from cart."""

        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self) -> None:
        """Save cart in user session."""

        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def __iter__(self) -> dict:
        """Enumeration of elements in cart and receiving products from database."""

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self) -> int:
        """Counting the number of units of products in cart."""

        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self) -> int:
        """Counting the total price of products in cart."""

        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    def clear(self) -> None:
        """Deleting cart from user session"""

        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

