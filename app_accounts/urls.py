from django.contrib.auth.views import LoginView
from django.urls import path

from app_accounts.forms import LoginForm
from app_accounts.views import personal_account_view, RegistrationView, logout_view

app_name = 'app_accounts'

urlpatterns = [
    path('', personal_account_view, name='personal_account'),
    path('login/', LoginView.as_view(
        template_name='app_accounts/login_page.html',
        authentication_form=LoginForm,
        redirect_authenticated_user=True
    ), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', logout_view, name='logout')
]
