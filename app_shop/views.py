from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View
from app_newsletter.forms import NewsletterEmailForm
from app_newsletter.models import NewsletterEmail
from app_shop.models import Product, Category


class MainPageView(View):
    """View for rendering and post-processing main_page.html"""

    def get(self, request) -> HttpResponse:
        products = Product.objects.select_related('category').all()
        categories = Category.objects.all().order_by('id')
        template = 'app_shop/main_page.html'
        return render(request, template, context={'products': products, 'categories': categories})

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        form = NewsletterEmailForm(request.POST)
        email = form.cleaned_data['email']
        if form.is_valid() and not NewsletterEmail.objects.filter(email=email):
            form.save()
        return HttpResponseRedirect('/')


class MainPageDetailView(View):
    """View for rendering and post-processing main_page.html detailed by category"""
    def get(self, request, category_pk: int) -> HttpResponse:
        products = Product.objects.filter(category=category_pk)
        categories = Category.objects.all().order_by('id')
        category = Category.objects.get(id=category_pk)
        context = {
            'products': products,
            'categories': categories,
            'category': category
        }
        template = 'app_shop/main_page_detail.html'
        return render(request, template, context=context)

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        return MainPageView().post(request)
