from textwrap import dedent

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .country import Country


class Location(models.Model):
    """
    Represents a geographical location unit within a faceted hierarchy,
    such as regions, municipalities, city areas, or streets. This model
    is designed to support hierarchical browsing, filtering and
    organization of properties within specific geographical contexts.
    """

    LOCATION_TYPE_CHOICES = [
        ("region", _("Region (e.g., Capital Region)")),
        ("municipality", _("Municipality (e.g., Copenhagen Municipality)")),
        ("city_area", _("City Area/District (e.g., København Ø)")),
        ("street", _("Street (e.g., Åfløjen)")),
    ]

    name = models.CharField(
        max_length=255,
        help_text=dedent(
            _(
                """
            The specific name of this location unit (e.g., 'København Ø'
            for a city area, 'Åfløjen' for a street). This is the primary
            label for the geographical unit.
        """
            ).strip()
        ),
    )
    slug = models.SlugField(
        max_length=80,
        unique=True,
        help_text=(
            "Unique, URL-safe identifier for this geographic area (e.g., region, district, "
            "neighborhood, or street). Generated from the name and used for building "
            "navigable routes, filters, and internal queries (e.g., 'osterbro', 'kobenhavn-v'). "
            "Helps support faceted navigation and search paths across different hierarchy levels."
        ),
    )
    location_type = models.CharField(
        max_length=50,
        choices=LOCATION_TYPE_CHOICES,
        help_text=dedent(
            _(
                """
            The type of geographical unit this location represents
            (e.g., 'region', 'municipality', 'city_area', 'street').
            This categorizes the location within the hierarchy.
        """
            ).strip()
        ),
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        help_text=dedent(
            _(
                """
            A foreign key to another Location instance, representing the
            parent location in the hierarchy (e.g., a 'city_area' might
            have a 'municipality' as its parent). This field is null
            for top-level locations (e.g., regions or countries).
        """
            ).strip()
        ),
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="locations",
        help_text=dedent(
            _(
                """
            The country this location unit primarily belongs to. This
            helps in scoping top-level locations and ensuring all
            hierarchical units are linked to a specific country.
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
            Optional central latitude coordinate for this location unit.
            Useful for displaying a central point on a map for broader
            areas like streets or city areas.
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
            Optional central longitude coordinate for this location unit.
            Useful for displaying a central point on a map for broader
            areas like streets or city areas.
        """
            ).strip()
        ),
    )

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        # Ensures that a location name and type is unique within its
        # country context, preventing duplicate entries for the same
        # type of location within a country.
        unique_together = (
            "name",
            "location_type",
            "country",
        )
        ordering = ["name"]

    def __str__(self) -> str:
        repr = f"{self.name} ({self.get_location_type_display()})"
        if self.parent:
            return f"{repr} in {self.parent.name}"
        return repr

    def clean(self) -> None:
        super().clean()
        # Custom validation to ensure hierarchical integrity:
        # A child location must belong to the same country as its parent.
        if self.parent and self.parent.country != self.country:
            raise ValidationError(
                _("A location's parent must belong to the same country.")
            )
