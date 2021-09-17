from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from account.models import Account, Address, Customer


# Register your models here.
class AccountAdminConfig(UserAdmin):
    model = Account
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_admin', 'is_superuser', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('username',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    fieldsets = (
        (_('Required'), {'fields': ('username', 'email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


admin.site.register(Account, AccountAdminConfig)
admin.site.register(Address)
admin.site.register(Customer)