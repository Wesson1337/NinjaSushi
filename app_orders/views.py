from django.shortcuts import render
from django.views.generic import DetailView
from app_orders.models import Order


class OrderHistoryDetailView(DetailView):
    template_name = 'app_orders/order_history_detail_page.html'
    queryset = Order.objects.all()
    context_object_name = 'order'
