from django.db import models

from .timetracking import TimeTracking


class Address(TimeTracking):
    street = models.CharField(max_length=255, help_text="Enter the street address")
    city = models.CharField(max_length=255, help_text="Enter the city")
    region = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Enter the region, state, or province (if applicable).",
    )
    postal_code = models.CharField(
        max_length=20, help_text="Enter the postal code or ZIP code."
    )
    country = models.CharField(max_length=255, help_text="Enter the country.")

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        # not specifying the ordering as it is not improtant here. Also
        # ordering large querysets can be resource-intensive

    def __str__(self):
        if self.region:
            return f"{self.street}, {self.city}, {self.region} {self.postal_code}, {self.country}"
        else:
            return f"{self.street}, {self.city}, {self.postal_code}, {self.country}"
