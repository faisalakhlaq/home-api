# type: ignore
from django.contrib import admin

from apps.core.models import Address, Genre, Status


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "model", "active", "description", "sorting_order"]
    list_editable = ["name", "model", "active", "description", "sorting_order"]
    list_filter = ["active"]
    search_fields = [
        "id",
        "name",
        "description",
    ]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "model", "active", "description", "sorting_order"]
    list_editable = ["name", "model", "active", "description", "sorting_order"]
    list_filter = ["active"]
    search_fields = [
        "id",
        "name",
        "description",
    ]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["id", "street", "city", "region", "postal_code", "country"]
    list_editable = ["street", "city", "region", "postal_code", "country"]
    list_filter = ["active"]
    search_fields = [
        "id",
        "name",
        "description",
    ]
