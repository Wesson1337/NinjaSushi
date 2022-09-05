from django.contrib import admin


class NewsletterEmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_on']