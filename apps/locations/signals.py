from typing import Any

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import City, Location


def generate_slug(
    instance: City | Location, source_field: str = "name", target_field: str = "slug"
) -> None:
    if not getattr(instance, target_field):
        setattr(instance, target_field, slugify(getattr(instance, source_field)))


@receiver(pre_save, sender=City)
def set_city_slug(sender: City, instance: City, **kwargs: Any) -> None:
    generate_slug(instance)


@receiver(pre_save, sender=Location)
def set_location_slug(sender: Location, instance: Location, **kwargs: Any) -> None:
    generate_slug(instance)
