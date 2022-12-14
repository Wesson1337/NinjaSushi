from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import DetailView
from app_orders.models import Order, OrderItem


class OrderHistoryDetailView(DetailView):
    model = Order
    template_name = 'app_orders/order_history_detail_page.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        order = self.object
        order_items = OrderItem.objects.select_related('product').filter(order=self.kwargs.get('pk'))
        context = {'order_items': order_items, 'order': order}
        return context


def repeat_order_view(request, order_id: int) -> HttpResponseRedirect:
    order = Order.objects.get(id=order_id)
    order.repeat_order(request)
    return redirect('app_cart:cart_view')
