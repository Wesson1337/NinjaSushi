from django.urls import path
from app_accounts.views import personal_account_view, LoginPageView

app_name = 'app_accounts'

urlpatterns = [
    path('', personal_account_view, name='personal_account'),
    path('login/', LoginPageView.as_view(), name='login')
]
