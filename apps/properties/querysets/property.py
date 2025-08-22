from typing import List

from django.db.models import (
    Case,
    Exists,
    IntegerField,
    OuterRef,
    Prefetch,
    QuerySet,
    When,
)

from apps.properties.models import Property, PropertyImage
from apps.favorites.models import UserFavoriteProperty


def property_list_queryset(
    filter: List[float | int | str] | None = None,
    filter_key: str = "id",
    country_code: str | None = None,
    status: str | List[str] | None = None,
    user_id: int | None = None,
) -> QuerySet[Property]:
    """
    Constructs and returns a queryset for listing `Property` objects with
    optional filters and annotations.

    Queryset prefetches a single, primary image for each property if one
    exists, or a fallback image otherwise.

    Parameters
    ----------
    filter : list[int | float | str], optional
        If provided, filters the queryset using the provided `filter_key` (e.g., 'id').
    filter_key : str, default='id'
        Field name to use when filtering the queryset by `filter`.
    country_code : str, optional
        Filters the queryset by this country code. Assumed to be upper-cased ISO2.
    status : str or list[str], optional
        Filters the queryset by one or more status values (e.g., 'ACTIVE', 'SOLD').
    user_id : int, optional
        If provided, annotates each property with an `is_favorite` boolean indicating
        if the property is marked as a favorite by this user.

    Returns
    -------
    QuerySet[Property]
        A queryset of `Property` objects with:
        - Preloaded images
        - Minimal selected fields for list views
        - Optional user-specific favorite annotation
    """
    # Use Prefetch with a custom queryset to get only the one image we need.
    # The Case statement orders images, prioritizing is_primary=True (value 0).
    # `image` is included to ensure the image path is fetched.
    image_queryset = PropertyImage.objects.order_by(
        Case(
            When(is_primary=True, then=0),
            default=1,
            output_field=IntegerField(),
        ),
        "id",
    )

    lookup = "__".join([filter_key, "in"])
    base_query = (
        Property.objects.filter(**{lookup: filter})
        if filter
        else Property.objects.all()
    )
    list_qs = base_query.prefetch_related(
        Prefetch(
            "property_images", queryset=image_queryset, to_attr="prefetched_images"
        )
    ).only(
        "id",
        "property_type",
        "created_at",
        "price",
        "price_currency",
        "total_rooms",
        "area",
        "energy_class",
        "street_name",
        "street_number",
        "postal_code",
        "city",
    )

    if country_code:
        list_qs = list_qs.filter(country_code=country_code.upper())

    if status:
        if not isinstance(status, list):
            status = [status]
        list_qs = list_qs.filter(status__in=status)

    if user_id:
        # Annotate each property with a boolean indicating whether it's a favorite
        # of the user_id
        list_qs = list_qs.annotate(
            is_favorite=Exists(
                UserFavoriteProperty.objects.filter(
                    user_id=user_id, property_id=OuterRef("pk")
                )
            )
        )

    return list_qs
