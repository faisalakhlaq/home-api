from typing import List

from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes

import django_filters
from django_filters.rest_framework import filters as django_rest_filters


class NumberInFilter(django_rest_filters.BaseInFilter, django_rest_filters.NumberFilter):  # type: ignore
    pass


class CharInFilter(django_rest_filters.BaseInFilter, django_rest_filters.CharFilter):  # type: ignore
    pass


class CustomFilterSet(django_filters.FilterSet):  # type: ignore
    """
    A custom FilterSet base class that automatically generates `OpenApiParameter`
    objects for all defined filters.

    This class is intended to be used with `drf-spectacular` and provides a
    convenient way to document your `django-filter` based filters in the
    Swagger UI and OpenAPI schema without manually defining each parameter.

    Usage:
    - Inherit from this class instead of `django_filters.FilterSet`.
    - In your `views.py`, use the `.spectacular_parameters()` class method
      within the `parameters` list of the `@extend_schema` decorator.
    - Use the `exclude_fields` parameter to omit filters that you are
      documenting manually (e.g., a required field with examples).

    Example:
    ```python
    # filters.py
    from core.utils.spectacular import OpenApiFilterSet

    class PropertyFilter(OpenApiFilterSet):
        city = django_filters.CharFilter(field_name="city", lookup_expr="iexact")
        min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
        max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

        class Meta:
            model = Property
            fields = ()

    # views.py
    from drf_spectacular.utils import extend_schema, OpenApiParameter

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="country_code",
                description="ISO 3166-1 country code",
                required=True,
                type=str,
            ),
            *PropertyFilter.spectacular_parameters()
        ]
    )
    class PropertyViewSet(viewsets.ModelViewSet):
        # ...
    ```
    """

    @classmethod
    def spectacular_parameters(
        cls, exclude_fields: List[str] | None = None
    ) -> List[OpenApiParameter]:
        """
        Generates a list of `OpenApiParameter` objects for the FilterSet.

        This method introspects the filters defined on the class and creates
        an `OpenApiParameter` for each, inferring the type and description
        from the filter field.

        Args:
            exclude_fields (list[str], optional): A list of filter field names
                to exclude from the generated parameters. This is useful for
                filters you want to define manually (e.g., to add examples,
                make them required, or provide a more detailed description).
                Defaults to an empty list.

        Returns:
            list[OpenApiParameter]: A list of `drf-spectacular` OpenApiParameter
                objects, ready to be used in an `extend_schema` decorator.

        Example:
        ```python
        # In a view's extend_schema decorator:
        parameters=[
            # Manually define a required field with examples
            OpenApiParameter(
                name="country_code",
                description="ISO 3166-1 country code",
                required=True,
                type=str,
                examples=[...],
            ),
            # Automatically add all other filters
            *PropertyFilter.spectacular_parameters(exclude_fields=['country_code'])
        ]
        ```
        """
        if exclude_fields is None or not isinstance(exclude_fields, list):
            exclude_fields = []
        parameters = []

        for field_name, filter_field in cls.get_filters().items():
            if field_name in exclude_fields:
                continue

            param_name = field_name
            param_description = filter_field.label or f"Filter by {field_name}"
            param_type = OpenApiTypes.STR  # Default type

            if isinstance(
                filter_field,
                (
                    django_filters.NumberFilter,
                    django_filters.rest_framework.filters.NumberFilter,
                ),
            ):
                param_type = OpenApiTypes.NUMBER
                if filter_field.lookup_expr in ["gte", "lte"]:
                    param_name = f"{field_name}_{filter_field.lookup_expr}"
                    param_description = (
                        f"Filter by {field_name} (lookup: {filter_field.lookup_expr})"
                    )
            elif isinstance(
                filter_field,
                (django_filters.CharFilter, django_rest_filters.CharFilter),
            ):
                param_type = OpenApiTypes.STR
            elif isinstance(filter_field, (django_filters.UUIDFilter)):
                param_type = OpenApiTypes.UUID
            elif isinstance(filter_field, django_filters.DateFilter):
                param_type = OpenApiTypes.DATE
            elif isinstance(filter_field, django_filters.DateTimeFilter):
                param_type = OpenApiTypes.DATETIME

            parameters.append(
                OpenApiParameter(
                    name=param_name,
                    description=param_description,
                    type=param_type,
                    required=False,
                )
            )
        return parameters
