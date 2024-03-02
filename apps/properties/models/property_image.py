from typing import Any

from django.core.validators import FileExtensionValidator
from django.db import models

from apps.core.models import TimeTracking

from .property import Property


def property_image_path(instance: Any, filename: str) -> str:
    """Returns path for property image storage.

    Path for the image is constructed by creating property folder within the
    images folder. The property folder name is equal to DB ID of property object.
    """
    return "media/property/images/{0}/{1}".format(instance.id, filename)


class PropertyImage(TimeTracking):
    title = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional title  for the image.",
    )
    description = models.TextField(
        blank=True,
        help_text="Optional description for the image.",
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Primary image will be displayed first for the property.",
    )
    image = models.ImageField(
        upload_to=property_image_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["png", "jpg", "jpeg", "bmp", "gif"]
            ),
        ],
        help_text="Image of the property.",
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="property_images",
        help_text="Image belong to the given property.",
    )

    class Meta:
        verbose_name = "Property Image"
        verbose_name_plural = "Property Images"
