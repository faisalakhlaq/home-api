from textwrap import dedent

from django.db import models
from django.utils.translation import gettext_lazy as _

from .country import Country


class City(models.Model):
    """
    Represents a specific city, linked to its respective country.
    This model stores the official or native city names, geographic
    coordinates for mapping purposes, and supports translations
    for international display. It serves as a normalized reference
    for city data.
    """

    name = models.CharField(
        max_length=255,
        help_text=dedent(
            _(
                """
            The official or native name of the city (e.g., 'København'
            in Danish, 'Munich' in English/German). This is the primary
            identifier for the city within its country.
        """
            ).strip()
        ),
    )
    slug = models.SlugField(
        max_length=80,
        unique=True,
        help_text=(
            "URL-friendly, language-neutral identifier for the city. Typically generated "
            "from the native city name (e.g., 'kobenhavn' for 'København'). Used for clean "
            "and SEO-friendly URLs, internal API lookups, and routing logic. "
            "Recommended for use in frontend routing and internationalized applications."
        ),
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="cities",
        help_text=dedent(
            _(
                """
            A foreign key linking this city to its corresponding country.
            If the linked country record is deleted, all associated cities
            will also be removed from the database.
        """
            ).strip()
        ),
    )
    region = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=dedent(
            _(
                """
            An optional administrative region name within the country
            (e.g., 'Capital Region of Denmark', 'Bavaria' for Germany,
            'California' for USA). This field captures larger sub-national
            divisions that a city belongs to.
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
            The latitude coordinate of the city's approximate geographical
            center. This is used for general map positioning, displaying
            city-level markers, or calculating distances.
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
            The longitude coordinate of the city's approximate geographical
            center. This is used for general map positioning, displaying
            city-level markers, or calculating distances.
        """
            ).strip()
        ),
    )

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
        # Ensures that a city name is unique only within the context of a
        # specific country, allowing for cities with the same name in
        # different countries (e.g., 'London' in UK and Canada).
        unique_together = (
            "name",
            "country",
        )
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name}, {self.country.name}"
