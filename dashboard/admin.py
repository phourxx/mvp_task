from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "deposit", "role", "password")}),
    )
    add_fieldsets = (
        (None, {"fields": ("username", "deposit", "role", "password1",
                           "password2")}),
    )
    list_display = ("username", "deposit", "role")
    list_filter = ("is_staff", "is_superuser", "is_active", "role")
    search_fields = ("username",)
    ordering = ("username", "deposit",)


User_ = get_user_model()
admin.site.register(User_, UserAdmin)
admin.site.register(Product)
admin.site.register(DepositHistory)
admin.site.register(Inventory)
admin.site.register(Purchase)
