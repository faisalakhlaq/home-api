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

        # Apply property type filters if provided
        if property_types:
            base_qs = base_qs.filter(property_type__in=property_types)

        # Text search conditions
        text_filter = (
            Q(city__icontains=query)
            | Q(street_name__icontains=query)
            | Q(postal_code__icontains=query)
        )

        filtered = base_qs.filter(text_filter)

        return {
            "cities": filtered.values("city")
            .annotate(count=Count("id"))
            .order_by("-count")[:5],
            "streets": filtered.values("street_name", "postal_code")
            .annotate(count=Count("id"))
            .order_by("-count")[:5],
            "addresses": filtered.filter(
                Q(street_name__icontains=query) & Q(postal_code__icontains=query)
            ).values("street_name", "street_number", "postal_code")[:5],
            # Add filter counts for UI display
            "filter_counts": {
                "total": filtered.count(),
                "filtered": filtered.count() if property_types else None,
            },
        }
