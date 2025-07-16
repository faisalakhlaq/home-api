import datetime
from textwrap import dedent

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import Address, Genre, Status, TimeTracking


def validate_positive(value: int | float) -> None:
    if value is not None and value <= 0:
        raise ValidationError(_("Value must be positive."))


def current_year() -> int:
    """
    Returns the current year as an integer.
    """
    return datetime.date.today().year


def max_value_current_year(value: int) -> None:
    """
    Validator to ensure the provided year is not greater than the current year.

    Args:
        value (int): The year to validate.

    Raises:
        django.core.validators.ValidationError: If the value exceeds the
        current year.
    """
    return MaxValueValidator(current_year())(value)


class Property(TimeTracking):
    """
    Represents a real estate property listing with detailed attributes.

    This model stores comprehensive information about a property, including
    financial, physical, and administrative details. It inherits from
    TimeTracking for automatic creation and update timestamps.

    Attributes:
        price (DecimalField): The asking price of the property.
        price_currency (CharField): The 3-letter currency abbreviation for the
            price (e.g., "USD", "EUR").
        area (FloatField): The covered area of the property in square meters,
            representing indoor living space.
        total_area (FloatField): The total ground area of the property,
            including outdoor spaces.
        measured_area (FloatField, optional): The professionally measured area
            of the property, if available.
        total_rooms (FloatField, optional): The total number of rooms within
            the property.
        toilets (IntegerField, optional): The total number of toilet facilities.
        construction_year (IntegerField, optional): The year the property was
            built.
        renovation_year (IntegerField, optional): The most recent year of
            significant renovation.
        total_floors (IntegerField, optional): The total number of floors/stories.
        heating (CharField, optional): Description of the property's heating
            system.
        outer_walls (CharField, optional): Description of the primary outer
            wall material.
        roof_type (CharField, optional): Description of the roof type and
            material.
        description (TextField, optional): A detailed internal description of
            the property.
        address (ForeignKey): Link to the associated Address model.
        type (ForeignKey, optional): Link to the Genre (type) of the property.
        status (ForeignKey, optional): Link to the current Status of the
            property (e.g., For Sale).
        owner (ForeignKey, optional): Link to the User who created or owns the
            listing.
    """

    price = models.DecimalField(
        max_digits=19,  # Django's max for DecimalField
        decimal_places=2,
        validators=[validate_positive],
        help_text=_("The asking price of the property."),
    )
    price_currency = models.CharField(
        max_length=5,
        help_text=_(
            "Provide the 3-letter currency code for the price "
            "(e.g., 'USD', 'EUR', 'GBP')."
        ),
    )
    area = models.FloatField(
        validators=[validate_positive],
        help_text=_(
            dedent(
                """The covered area of the property in square meters.
            This refers to the total indoor living space, including all rooms,
            hallways, and any other enclosed spaces within the structure."""
            )
        ),
    )
    total_area = models.FloatField(
        validators=[validate_positive],
        help_text=_(
            dedent(
                """The total ground area of the property. This encompasses
            the entire land area upon which the property is built, including
            outdoor spaces such as yards, gardens, and driveways."""
            )
        ),
    )
    measured_area = models.FloatField(
        validators=[validate_positive],
        blank=True,
        null=True,
        help_text=_(
            "The officially measured and verified area of the property, "
            "typically used for legal or appraisal purposes."
        ),
    )
    total_rooms = models.FloatField(
        validators=[validate_positive],
        blank=True,
        null=True,
        help_text=_(
            dedent(
                """The total number of distinct rooms within the property,
            excluding bathrooms and kitchens unless specified otherwise."""
            )
        ),
    )
    toilets = models.IntegerField(
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text=_("The total number of toilet facilities in the property."),
    )
    construction_year = models.IntegerField(
        validators=[MinValueValidator(0), max_value_current_year],
        blank=True,
        null=True,
        help_text=_(
            "The year in which the main construction of the property was " "completed."
        ),
    )
    renovation_year = models.IntegerField(
        validators=[MinValueValidator(0), max_value_current_year],
        blank=True,
        null=True,
        help_text=_(
            "The most recent year in which significant renovations or major "
            "updates were performed on the property."
        ),
    )
    total_floors = models.IntegerField(
        validators=[MinValueValidator(1)],
        blank=True,
        null=True,
        help_text=_(
            "The total number of floors or stories that the property comprises."
        ),
    )
    heating = models.CharField(
        max_length=255,
        blank=True,
        help_text=_(
            dedent(
                """Detailed description of the heating system, e.g.,
            'Central heating with gas furnace' or 'Electric baseboard heating'."""
            )
        ),
    )
    outer_walls = models.CharField(
        max_length=255,
        blank=True,
        help_text=_(
            "The primary material used for the exterior walls, "
            "e.g., 'Brick', 'Stucco', 'Wood siding'."
        ),
    )
    roof_type = models.CharField(
        max_length=255,
        blank=True,
        help_text=_(
            "The type of roofing material and style, "
            "e.g., 'Tile', 'Shingle', 'Flat roof'."
        ),
    )
    description = models.TextField(
        blank=True,
        help_text=_(
            dedent(
                """A comprehensive internal description highlighting the
            key features, amenities, and unique selling points of the property
            for administrative use."""
            )
        ),
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.RESTRICT,
        related_name="address_properties",
        help_text=_("The physical address where the property is located."),
    )
    type = models.ForeignKey(
        Genre,
        on_delete=models.RESTRICT,
        related_name="genre_properties",
        help_text=_(
            "The classification or genre of the property (e.g., 'Residential', "
            "'Commercial', 'Apartment', 'House')."
        ),
        blank=True,
        null=True,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.RESTRICT,
        related_name="status_properties",
        help_text=_(
            "The current transactional status of the property (e.g., 'For Sale', "
            "'Under Contract', 'Sold', 'Rented')."
        ),
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_(
            "The user account associated with the creation or current ownership "
            "of this property listing."
        ),
    )

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")

    def __str__(self) -> str:
        """Returns a string representation of the property."""
        return _(
            "Property (Rooms: {total_rooms}, Price: {price} {currency}, "
            "Area: {area} sqm)"
        ).format(
            total_rooms=self.total_rooms,
            price=self.price,
            currency=self.price_currency,
            area=self.area,
        )
