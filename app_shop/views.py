from django.shortcuts import render

from app_shop.models import Product


def main_page_view(request):
    products = Product.objects.all()
    return render(request, 'app_shop/main_page.html', context={'products': products})
