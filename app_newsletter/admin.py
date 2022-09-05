from django.contrib import admin
from app_newsletter.models import NewsletterEmail


@admin.register(NewsletterEmail)
class NewsletterEmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'created']
