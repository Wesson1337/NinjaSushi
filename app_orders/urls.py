from django.urls import path

from app_orders.views import OrderHistoryDetailView

app_name = 'app_orders'

urlpatterns = [
    path('<int:pk>/', OrderHistoryDetailView.as_view(), name='order_history_detail')
]