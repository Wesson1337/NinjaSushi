from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView

from app_accounts.forms import RegistrationForm


def personal_account_view(request):
    if request.user.is_authenticated:
        orders = request.user.orders.all().order_by('-created')
        return render(request, 'app_accounts/personal_account_page.html', context={'orders': orders})
    return redirect('app_accounts:login')


class RegistrationView(FormView):
    template_name = 'app_accounts/registration_page.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        """Registration and login if form is valid"""
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('app_accounts:personal_account')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('app_shop:main_page')
