from textwrap import dedent

from django.db import models
from django.utils.translation import gettext_lazy as _

from .city import City


class CityTranslation(models.Model):
    """
    Provides translations for city names, enabling the application to
    display city names in various languages. This is essential for
    supporting a global user base and providing localized content.
    """

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="translations",
        help_text=dedent(
            _(
                """
            The city for which this translation is provided. If the
            associated city record is deleted, this translation will
            also be automatically removed.
        """
            ).strip()
        ),
    )
    language = models.CharField(
        max_length=10,
        help_text=dedent(
            _(
                """
            The ISO 639-1 language code for this translation (e.g., 'en'
            for English, 'fr' for French, 'de' for German). This code
            specifies the target language for the translated name.
        """
            ).strip()
        ),
    )
    translated_name = models.CharField(
        max_length=255,
        help_text=dedent(
            _(
                """
            The name of the city in the specified language (e.g., if the
            native city name is 'København', its 'en' translated_name
            would be 'Copenhagen').
        """
            ).strip()
        ),
    )

    class Meta:
        verbose_name = _("City Translation")
        verbose_name_plural = _("City Translations")
        # Ensures that there is only one translation for a specific city
        # in a given language, preventing duplicate translation entries.
        unique_together = (
            "city",
            "language",
        )

    def __str__(self) -> str:
        return f"{self.city.name} ({self.language}): {self.translated_name}"
