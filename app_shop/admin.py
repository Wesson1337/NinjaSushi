from django.contrib import admin
from app_shop.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
