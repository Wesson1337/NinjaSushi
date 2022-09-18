from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django import forms

from app_accounts.models import CustomUser


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input-field'


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input-field'

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'phone_number', 'date_of_birth', 'password1', 'password2')

