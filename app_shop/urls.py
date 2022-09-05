from django.urls import path
from app_shop.views import MainPageView, MainPageDetailView

app_name = 'app_shop'

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('<int:category_pk>', MainPageDetailView.as_view(), name='main_page_detail')
]
