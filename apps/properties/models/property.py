import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.core.models import Address, Genre, Status, TimeTracking


def current_year() -> int:
    return datetime.date.today().year


def max_value_current_year(value: int) -> None:
    return MaxValueValidator(current_year())(value)


class Property(TimeTracking):
    price = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Price of the property.",
    )
    price_currency = models.CharField(
        max_length=5,
        help_text="Provide the currency abbreviations for the price. (3-letter acronym for the currency).",
    )
    area = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="""Coverd area of the property in square meters.The covered area
        of a property typically refers to the total indoor living area, including
        all rooms, hallways, and any other enclosed spaces within the structure.""",
    )
    total_area = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="""Total ground area of the property. The total ground space
        available refers to the entire area of land upon which the house is built,
        including any outdoor spaces such as yards, gardens, driveways, etc.""",
    )
    measured_area = models.FloatField(
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )
    total_rooms = models.FloatField(
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text="Total number of rooms in the property.",
    )
    toilets = models.IntegerField(
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text="Total number of toilets in the property.",
    )
    construction_year = models.IntegerField(
        validators=[MinValueValidator(0), max_value_current_year],
        blank=True,
        null=True,
        help_text="Year in which the property was built.",
    )
    renovation_year = models.IntegerField(
        validators=[MinValueValidator(0), max_value_current_year],
        blank=True,
        null=True,
        help_text="Year in which the property was built.",
    )
    total_floors = models.IntegerField(
        validators=[MinValueValidator(1)],
        blank=True,
        null=True,
        help_text="Total number of floors and stories the property conprises of.",
    )
    heating = models.CharField(
        max_length=255,
        blank=True,
        help_text="""e.g. Heating installation. e.g. Central heating with one
        heating unit.""",
    )
    outer_walls = models.CharField(max_length=255, blank=True, help_text="e.g. Brick.")
    roof_type = models.CharField(max_length=255, blank=True, help_text="e.g. Tile.")
    description = models.TextField(blank=True)
    address = models.ForeignKey(
        Address,
        on_delete=models.RESTRICT,
        related_name="address_properties",
        help_text="Address of the property.",
    )
    type = models.ForeignKey(
        Genre,
        on_delete=models.RESTRICT,
        related_name="genre_properties",
        help_text="Type | Genre of the property.",
        blank=True,
        null=True,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.RESTRICT,
        related_name="status_properties",
        help_text="Status of the property.",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def __str__(self) -> str:
        return f"Rooms: {self.total_rooms}, Price={self.price}, Covered are={self.area}"
