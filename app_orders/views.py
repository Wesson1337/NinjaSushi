from django.shortcuts import render
from django.views.generic import DetailView
from app_orders.models import Order, OrderItem


class OrderHistoryDetailView(DetailView):
    model = Order
    template_name = 'app_orders/order_history_detail_page.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        order_items = OrderItem.objects.select_related('product').filter(order=self.kwargs.get('pk'))
        order_user = self.object.user
        context = {'order_items': order_items, 'order_user': order_user}
        return context
