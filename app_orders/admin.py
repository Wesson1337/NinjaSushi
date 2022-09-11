from django.contrib import admin
from app_orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'get_total_cost']
    list_filter = ['payment_method', 'paid', 'created', 'updated']
    search_fields = ['id', 'user__username', 'name']
    inlines = [OrderItemInline]
