from typing import Any

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import City, Location


def generate_slug(
    instance: City | Location, source_field: str = "name", target_field: str = "slug"
) -> None:
    if getattr(instance, target_field):
        return

    base_slug = slugify(getattr(instance, source_field))
    model_class = instance.__class__

    # For Cities: include country code and disambiguate duplicates
    if isinstance(instance, City):
        unique_slug = f"{base_slug}-{instance.country.code.lower()}"
        counter = 1
        while (
            model_class.objects.filter(slug=unique_slug)
            .exclude(pk=instance.pk)
            .exists()
        ):
            unique_slug = f"{base_slug}-{instance.country.code.lower()}-{counter}"
            counter += 1

    # For Locations: include parent slug if available
    elif isinstance(instance, Location) and instance.parent:
        parent_slug = instance.parent.slug or slugify(instance.parent.name)
        unique_slug = f"{base_slug}-{parent_slug}"
        counter = 1
        while (
            model_class.objects.filter(slug=unique_slug)
            .exclude(pk=instance.pk)
            .exists()
        ):
            unique_slug = f"{base_slug}-{parent_slug}-{counter}"
            counter += 1

    # Fallback for root locations
    else:
        unique_slug = base_slug
        counter = 1
        while (
            model_class.objects.filter(slug=unique_slug)
            .exclude(pk=instance.pk)
            .exists()
        ):
            unique_slug = f"{base_slug}-{counter}"
            counter += 1

    setattr(instance, target_field, unique_slug)


@receiver(pre_save, sender=City)
def set_city_slug(sender: City, instance: City, **kwargs: Any) -> None:
    generate_slug(instance)


@receiver(pre_save, sender=Location)
def set_location_slug(sender: Location, instance: Location, **kwargs: Any) -> None:
    generate_slug(instance)
