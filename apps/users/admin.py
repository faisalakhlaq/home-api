# type: ignore
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "full_name",
        "is_staff",
        "is_active",
        "is_business_user",
        "is_company_admin",
    )
    search_fields = ("email", "first_name", "last_name", "full_name")
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "is_business_user",
        "is_company_admin",
    )
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "full_name")},  # Include full_name
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined")},
        ),
        (
            "Business Information",
            {"fields": ("is_business_user", "is_company_admin")},
        ),
    )

    # Add fieldsets for adding a new user (similar to above, but without last_login/date_joined)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password", "password2"),
            },
        ),
        (
            "Personal info",
            {"fields": ("first_name", "last_name")},
        ),
        (
            "Business Information",
            {"fields": ("is_business_user", "is_company_admin")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    # Ensure full_name is read-only in the admin change form as it's auto-generated
    readonly_fields = ("full_name",)


admin.site.register(User, CustomUserAdmin)
