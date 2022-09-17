from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django import forms

from app_accounts.models import CustomUser


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'input-field', 'id': 'username-input'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input-field', 'id': 'password-input'}
    ))


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'phone_number', 'date_of_birth', 'password1', 'password2')

