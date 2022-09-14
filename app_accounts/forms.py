from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django import forms


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
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        username = UsernameField(widget=forms.TextInput(
            attrs={'class': 'input-field', 'id': 'username-input'}
        ))
        password = forms.CharField(widget=forms.PasswordInput(
            attrs={'class': 'input-field', 'id': 'password-input'}
        ))
        first_name = forms.CharField(required=True, widget=forms.TextInput(
            attrs={'class': 'input-field', 'id': 'first-name-input'}
        ))
        phone_number = forms.CharField(required=True, widget=forms.TextInput(
            attrs={'class': 'input-field', 'placeholder': '+7(___)___-__-__', 'id': 'phone-number-input'}
        ))
        date_of_birth = forms.DateField(widget=forms.DateInput(
            attrs={'class': 'input-field', 'id': 'date_of-birth-input'}
        ))

