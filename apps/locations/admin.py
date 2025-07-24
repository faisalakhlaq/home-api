# type: ignore

from django.contrib import admin

from apps.locations.models import City, Country


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    fields = [field.name for field in City._meta.get_fields() if not field.is_relation]
    list_display = fields
    search_fields = fields


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    fields = [
        field.name for field in Country._meta.get_fields() if not field.is_relation
    ]
    list_display = fields
    search_fields = fields
