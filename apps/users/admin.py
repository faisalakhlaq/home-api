# type: ignore
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("is_business_user", "is_company_admin")}),
    )
    list_display = UserAdmin.list_display + (
        "is_business_user",
        "is_company_admin",
    )


admin.site.register(User, CustomUserAdmin)
