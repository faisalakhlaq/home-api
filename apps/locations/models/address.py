from textwrap import dedent

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeTracking

from .city import City


class Address(TimeTracking):
    """
    Represents a specific physical address for a property. This model
    stores granular address components (street, number, postal code)
    and precise geographic coordinates. It serves as the definitive,
    normalized source of address information and automatically generates
    a concatenated text field for simplified search operations.
    """

    street_name = models.CharField(
        max_length=255,
        help_text=dedent(
            _(
                """
            The primary name of the street or road without any house
            or building numbers (e.g., 'Åfløjen', 'Main Street').
        """
            ).strip()
        ),
    )
    street_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text=dedent(
            _(
                """
            The specific house, building, or unit number for the address
            (e.g., '40A', '123', 'Unit 5'). This field is optional as
            some addresses may not have a distinct number.
        """
            ).strip()
        ),
    )
    postal_code = models.CharField(
        max_length=20,
        help_text=dedent(
            _(
                """
            The postal code or ZIP code associated with this address.
            This is a critical component for mail delivery and often
            used in geographical lookups.
        """
            ).strip()
        ),
    )
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="addresses",
        help_text=dedent(
            _(
                """
            A foreign key linking this address to its corresponding city
            from the standardized City model. This ensures data integrity
            and consistency for city information.
        """
            ).strip()
        ),
    )
    latitude = models.FloatField(
        blank=True,
        null=True,
        help_text=dedent(
            _(
                """
            The precise latitude coordinate of the address. This is
            essential for accurate map positioning, displaying property
            markers, and performing geospatial queries.
        """
            ).strip()
        ),
    )
    longitude = models.FloatField(
        blank=True,
        null=True,
        help_text=dedent(
            _(
                """
            The precise longitude coordinate of the address. This is
            essential for accurate map positioning, displaying property
            markers, and performing geospatial queries.
        """
            ).strip()
        ),
    )

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self) -> str:
        parts = [self.street_name]
        if self.street_number:
            parts.append(self.street_number)
        parts.append(self.postal_code)
        if self.city:
            parts.append(self.city.name)
            parts.append(self.city.country.code)
        return " ".join(filter(None, parts))

    @property
    def formatted_address(self) -> str:
        return dedent(
            f"{self.street_name} "
            f"{self.street_number}, "
            f"{self.postal_code} "
            f"{self.city.name}, "
            f"{self.city.country.code}"
        )
