from django.shortcuts import render, redirect
from django.views import View


def personal_account_view(request):
    return render(request, 'app_accounts/personal_account_page.html')


class LoginPageView(View):
    """
    View for rendering login_page or redirecting to personal account if user is authenticated,
    and post-processing login_page.
     """
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('app_accounts:personal_account')
        return render(request, 'app_accounts/login_page.html')


