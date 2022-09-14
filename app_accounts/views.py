from django.shortcuts import render, redirect
from django.views import View


def personal_account_view(request):
    return render(request, 'app_accounts/personal_account_page.html')


