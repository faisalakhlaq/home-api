# type: ignore
from django.contrib import admin

from apps.properties.models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "price",
        "price_currency",
        "area",
        "total_area",
        "measured_area",
        "total_rooms",
        "toilets",
        "construction_year",
        "renovation_year",
        "total_floors",
        "heating",
        "outer_walls",
        "roof_type",
        "description",
        "address",
        "type",
        "status",
        "created_at",
        "updated_at",
    ]
    list_editable = [
        "price",
        "price_currency",
        "area",
        "total_area",
        "measured_area",
        "total_rooms",
        "toilets",
        "construction_year",
        "renovation_year",
        "total_floors",
        "heating",
        "outer_walls",
        "roof_type",
        "description",
        "address",
        "type",
        "status",
    ]
    list_filter = ["type", "status"]
    search_fields = [
        "id",
        "price",
        "price_currency",
        "area",
        "total_area",
        "measured_area",
        "total_rooms",
        "toilets",
        "construction_year",
        "renovation_year",
        "total_floors",
        "heating",
        "outer_walls",
        "roof_type",
        "description",
        "address",
        "type",
        "status",
        "created_at",
        "updated_at",
    ]
