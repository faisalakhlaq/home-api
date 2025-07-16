from typing import List

from django.db.models import BooleanField, Case, Prefetch, QuerySet, When

from apps.core.models import Address
from apps.favorites.models import UserFavoriteProperty
from apps.properties.models import Property, PropertyImage


def property_list_queryset(
    filter: List[float | int | str] | None = None,
    filter_key: str = "id",
    user_id: int | None = None,
) -> QuerySet[Property]:
    """Returns the list queryset for PropertyViewSet.

    If the filter is provided then the queryset will be filtered according to
    the given filter_key.

    If a user_id is provided then the properties_list will be populated with an
    extra field is_favorite. is_favorite indicates that the property is in user
    favorite properties.

    Example
    -------
    filter=[1, 2, 3]
    filter_key='id'

    Property.objects.filter(filter_key__in=[*filter])...
    """
    lookup = "__".join([filter_key, "in"])
    base_query = (
        Property.objects.filter(**{lookup: filter})
        if filter
        else Property.objects.all()
    )
    list_qs = (
        base_query.select_related("type")
        .prefetch_related(
            Prefetch(
                "property_images",
                queryset=PropertyImage.objects.only("image"),
            ),
            Prefetch(
                "address",
                queryset=Address.objects.only("postal_code", "street", "city"),
            ),
        )
        .only(
            "id",
            "type",
            "description",
            "created_at",
            "price",
            "price_currency",
            "address",
        )
    )
    if not user_id:
        return list_qs

    list_qs.prefetch_related(
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
