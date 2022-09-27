from django.urls import path

from app_orders.views import OrderHistoryDetailView, repeat_order_view

app_name = 'app_orders'

urlpatterns = [
    path('<int:pk>/', OrderHistoryDetailView.as_view(), name='order_history_detail'),
    path('repeat_order/<int:order_id>/', repeat_order_view, name='repeat_order')
]
