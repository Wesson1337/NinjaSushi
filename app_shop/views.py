from django.shortcuts import render

from app_shop.models import Product, Category


def main_page_view(request):
    """Renders main page"""
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all().order_by('id')
    return render(request, 'app_shop/main_page.html', context={'products': products, 'categories': categories})


def main_page_detail_view(request, category_pk):
    """Renders main page detailed by category"""
    products = Product.objects.filter(category=category_pk)
    categories = Category.objects.all().order_by('id')
    category = Category.objects.get(id=category_pk)
    context = {
        'products': products,
        'categories': categories,
        'category': category
    }
    return render(request, 'app_shop/main_page_detail.html', context=context)
