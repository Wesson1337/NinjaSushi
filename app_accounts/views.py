from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

from app_accounts.forms import RegistrationForm


def personal_account_view(request):
    if request.user.is_authenticated:
        return render(request, 'app_accounts/personal_account_page.html')
    return redirect('app_accounts:login')


class RegistrationView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('app_accounts:personal_account')
        form = RegistrationForm
        return render(request, 'app_accounts/registration_page.html', context={'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
        return redirect('app_accounts:personal_account')

