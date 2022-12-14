from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from app_newsletter.forms import NewsletterEmailForm
from app_newsletter.models import NewsletterEmail
from app_newsletter.tasks import newsletter_subscription_email_task
from app_shop.models import Product, Category


class MainPagePostView(View):
    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        form = NewsletterEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not NewsletterEmail.objects.filter(email=email):
                form.save()
                newsletter_subscription_email_task.delay(email)
        return redirect('app_shop:main_page')


class MainPageView(MainPagePostView):
    """View for rendering and post-processing main_page.html"""

    def get(self, request) -> HttpResponse:
        products = Product.objects.select_related('category').all()
        categories = Category.objects.all().order_by('id')
        template = 'app_shop/main_page.html'
        return render(request, template, context={'products': products, 'categories': categories})


class MainPageDetailView(MainPagePostView):
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
