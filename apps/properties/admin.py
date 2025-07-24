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
        "property_type",
        "status",
        "street_name",
        "street_number",
        "postal_code",
        "city",
        "region",
        "country_code",
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
        "property_type",
        "status",
    ]
    list_filter = ["property_type", "status"]
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
        "property_type",
        "status",
        "created_at",
        "updated_at",
    ]
