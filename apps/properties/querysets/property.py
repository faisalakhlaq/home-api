from typing import List

from django.db.models import BooleanField, Case, Prefetch, QuerySet, When

from apps.favorites.models import UserFavoriteProperty
from apps.properties.models import Property, PropertyImage


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
    lookup = "__".join([filter_key, "in"])
    base_query = (
        Property.objects.filter(**{lookup: filter})
        if filter
        else Property.objects.all()
    )
    list_qs = base_query.prefetch_related(
        Prefetch(
            "property_images",
            queryset=PropertyImage.objects.only("image"),
        ),
    ).only(
        "id",
        "property_type",
        "description",
        "created_at",
        "price",
        "price_currency",
        "city",
        "country_code",
    )

    if country_code:
        list_qs = list_qs.filter(country_code=country_code.upper())

    if status:
        if not isinstance(status, list):
            status = [status]
        list_qs = list_qs.filter(status__in=status)

    if not user_id:
        return list_qs

    list_qs = list_qs.prefetch_related(
        Prefetch(
            "favorite_user",
            queryset=UserFavoriteProperty.objects.filter(user=user_id),
            # to_attr="user_favorites",
        )
    )
    # Annotate each property with a boolean indicating whether it's a favorite
    # of the user_id
    return list_qs.annotate(
        is_favorite=Case(
            When(favorite_user__isnull=False, then=True),
            default=False,
            output_field=BooleanField(),
        )
    )
