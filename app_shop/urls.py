from django.urls import path
from app_shop.views import main_page_view, main_page_detail_view

app_name = 'app_shop'

urlpatterns = [
    path('', main_page_view, name='main_page'),
    path('<int:category_pk>', main_page_detail_view, name='main_page_detail')
]
