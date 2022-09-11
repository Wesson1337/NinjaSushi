from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app_accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "phone_number", "is_staff", "date_joined")

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Личная информация', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth')
        }),
        ('Доступы', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Активность', {
            'fields': ('last_login', 'date_joined')
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password', 'password2')
        }),
        ('Личная информация', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth')
        }),
        ('Доступы', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Активность', {
            'fields': ('last_login', 'date_joined')
        })
    )
