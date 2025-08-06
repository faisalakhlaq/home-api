from textwrap import dedent

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator, MinLengthValidator


class Country(models.Model):
    """
    Represents a country, adhering to the ISO 3166-1 Alpha-2 standards for
    country codes. This model provides a standardized and internationally
    recognized list of countries, crucial for internationalization and
    ensuring data consistency across the application.
    """

    code = models.CharField(
        max_length=2,
        unique=True,
        validators=[MinLengthValidator(2), MaxLengthValidator(2)],
        help_text=dedent(
            _(
                """
            The ISO 3166-1 Alpha-2 country code (e.g., 'DK' for Denmark,
            'US' for United States). This two-letter code is a globally
            recognized and unique identifier for each country, essential
            for standardized data representation and integration with
            external services.
        """
            ).strip()
        ),
    )
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=dedent(
            _(
                """
            The common English name of the country (e.g., 'Denmark',
            'Germany'). This name serves as the primary display name
            for the country in the application's English interface.
        """
            ).strip()
        ),
    )
    native_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=dedent(
            _(
                """
            The name of the country in its local or native language
            (e.g., 'Danmark' for Denmark, 'Deutschland' for Germany).
            This field is optional but highly valuable for providing
            a fully localized user experience.
        """
            ).strip()
        ),
    )

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        ordering = ["name"]  # Orders countries alphabetically by their English name

    def __str__(self) -> str:
        return self.name
