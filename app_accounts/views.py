from django.shortcuts import render


def personal_account_view(request):
    return render(request, 'app_accounts/personal_account_page.html')
