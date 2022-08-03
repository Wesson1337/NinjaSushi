from django.shortcuts import render

from app_shop.models import Product, Category


def main_page_view(request):
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()
    return render(request, 'app_shop/main_page.html', context={'products': products, 'categories': categories})
