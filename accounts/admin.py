from django.contrib import admin

from .models import Account
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display = ['first_name', 'last_name', 'username',
                    'email', 'last_login', 'date_joined', 'is_active']
    list_display_links = ['first_name', 'last_name']
    readonly_fields = ['last_login', 'date_joined', ]
    ordering = ['-date_joined']

    filter_horizontal = ()
    fieldsets = ()
    list_filter = ()


    # Register your models here.
admin.site.register(Account, AccountAdmin)
