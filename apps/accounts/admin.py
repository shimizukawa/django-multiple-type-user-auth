from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import FrontUser, CustomerUser, SupporterUser


# @admin.register(FrontUser)
class FrontUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {
            'fields': ('is_active',),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_active', 'last_login')
    list_filter = ('is_active',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


@admin.register(CustomerUser)
class CustomerUserAdmin(FrontUserAdmin):
    fieldsets = (
        FrontUserAdmin.fieldsets[0],
        ('Customer', {'fields': ('tel',)}),
    ) + FrontUserAdmin.fieldsets[1:]
    list_display = ('email', 'tel', 'is_active', 'last_login')


@admin.register(SupporterUser)
class SupporterUserAdmin(FrontUserAdmin):
    fieldsets = (
        FrontUserAdmin.fieldsets[0],
        ('Supporter', {'fields': ('organization',)}),
    ) + FrontUserAdmin.fieldsets[1:]
    list_display = ('email', 'organization', 'is_active', 'last_login')
