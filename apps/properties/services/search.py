from typing import Any, Dict, List

from django.db.models import Count, Q

from apps.properties.models import Property, PropertyStatus


class PropertySearch:
    @staticmethod
    def quick_search(
        query: str,
        country_code: str,
        property_types: List[str] | None = None,
        status: List[str] | str | None = None,
    ) -> Dict[str, Any]:
        base_qs = Property.objects.filter(country_code=country_code)

        if not status:
            status = [PropertyStatus.ACTIVE]
        elif not isinstance(status, list):
            status = [status]

        base_qs = base_qs.filter(status__in=status)

        if property_types:
            base_qs = base_qs.filter(property_type__in=property_types)

        # Get cities that contain the query in their city name
        cities_qs = base_qs.filter(city__icontains=query)
        cities = cities_qs.values("city").annotate(count=Count("id")).order_by("-count")

        # Get streets that contain the query in their street name
        streets_qs = base_qs.filter(street_name__icontains=query)
        streets = (
            streets_qs.values("street_name", "postal_code", "city")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        # Get addresses that contain the query in either street name or postal code
        address_qs = base_qs.filter(
            Q(street_name__icontains=query) | Q(postal_code__icontains=query)
        )
        addresses = address_qs.values(
            "street_name", "street_number", "postal_code", "city"
        )

        return {
            "cities": cities,
            "streets": streets,
            "addresses": addresses,
            # "filter_counts": {
            #     "total": (cities_qs.count() + streets_qs.count() + address_qs.count()),
            #     "filtered": base_qs.count() if property_types else None,
            # },
        }
