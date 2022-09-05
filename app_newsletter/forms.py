from django.forms import ModelForm
from .models import NewsletterEmail


class NewsletterEmailForm(ModelForm):
    class Meta:
        model = NewsletterEmail
        fields = ['email']
