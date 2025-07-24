import datetime
from textwrap import dedent

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeTracking
from apps.locations.models import Address


def validate_positive(value: int | float) -> None:
    if value is not None and value <= 0:
        raise ValidationError(_("Value must be positive."))


def current_year() -> int:
    """
    Returns the current year as an integer.
    """
    return datetime.date.today().year


def validate_max_current_year(value: int) -> None:
    """
    Validator to ensure the provided year is not greater than the current year.

    Args:
        value (int): The year to validate.

    Raises:
        django.core.validators.ValidationError: If the value exceeds the
        current year.
    """
    return MaxValueValidator(current_year())(value)


class PropertyType(models.TextChoices):
    # For detail of each choice check the seed/genre.py
    SINGLE_FAMILY = "SINGLE_FAMILY", _("Single-family detached home")
    APARTMENT = "APARTMENT", _("Apartment")
    CONDOMINIUM = "CONDOMINIUM", _("Condominium (Condo)")
    TOWNHOUSE = "TOWNHOUSE", _("Townhouse")
    DUPLEX = "DUPLEX", _("Duplex")
    TRIPLEX = "TRIPLEX", _("Triplex")
    COOP = "COOP", _("Co-operative housing (Co-op)")
    FARMHOUSE = "FARMHOUSE", _("Farmhouse")
    MANSION = "MANSION", _("Mansion")
    LAND = "LAND", _("Land / Ground")
    BOATHOUSE = "BOATHOUSE", _("Boathouse")
    RECREATIONAL = "RECREATIONAL", _("Recreational residence")
    COUNTRY_HOME = "COUNTRY_HOME", _("Country property")
    COTTAGE = "COTTAGE", _("Cottage")
    TINY_HOME = "TINY_HOME", _("Tiny home")
    MOBILE_HOME = "MOBILE_HOME", _("Mobile home")
    PENTHOUSE = "PENTHOUSE", _("Penthouse")
    LOFT = "LOFT", _("Loft")
    MULTI_UNIT = "MULTI_UNIT", _("Multi-family / Multi-unit property")
    MIXED_USE = "MIXED_USE", _("Mixed-use property")
    COMMERCIAL = "COMMERCIAL", _("Commercial space")
    INDUSTRIAL = "INDUSTRIAL", _("Industrial property")
    OFFICE = "OFFICE", _("Office space")
    WAREHOUSE = "WAREHOUSE", _("Warehouse")


class PropertyStatus(models.TextChoices):
    # For detail of each choice check the seed/status.py
    ACTIVE = "ACTIVE", _("Active")
    COMING_SOON = "COMING_SOON", _("Coming soon")
    UNDER_CONTRACT = "UNDER_CONTRACT", _("Under contract")
    PENDING = "PENDING", _("Pending")
    SOLD = "SOLD", _("Sold")
    LEASED = "LEASED", _("Leased")
    AUCTION = "AUCTION", _("Auction")
    OFF_MARKET = "OFF_MARKET", _("Off market")
    EXPIRED = "EXPIRED", _("Expired")
    WITHDRAWN = "WITHDRAWN", _("Withdrawn")
    CANCELED = "CANCELED", _("Canceled")
    DRAFT = "DRAFT", _("Draft")


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
        property_type (ForeignKey, optional): Link to the Genre (type) of the property.
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
                """The covered area of the property in square meters (m²).
            This refers to the total indoor living space, including all rooms,
            hallways, and any other enclosed spaces within the structure."""
            )
        ),
    )
    total_area = models.FloatField(
        validators=[validate_positive],
        help_text=_(
            dedent(
                """The total ground area of the property (m²). This encompasses
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
            "typically used for legal or appraisal purposes (m²)."
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
        validators=[MinValueValidator(0), validate_max_current_year],
        blank=True,
        null=True,
        help_text=_(
            "The year in which the main construction of the property was " "completed."
        ),
    )
    renovation_year = models.IntegerField(
        validators=[MinValueValidator(0), validate_max_current_year],
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
    property_type = models.CharField(
        max_length=255,
        choices=PropertyType.choices,
        help_text=_(
            "The classification or genre of the property (e.g., 'Residential', "
            "'Commercial', 'Apartment', 'House')."
        ),
    )
    status = models.CharField(
        max_length=255,
        choices=PropertyStatus.choices,
        default=PropertyStatus.ACTIVE,
        help_text=_(
            "The current transactional status of the property (e.g., 'For Sale', "
            "'Under Contract', 'Sold', 'Rented')."
        ),
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
    available_from = models.DateField(
        null=True,
        blank=True,
        help_text=_("When can the buy move in."),
    )
    energy_class = models.CharField(
        null=True,
        blank=True,
        help_text=_(
            "What is the energy class of the property. (e.g. A, B, C, D, E, F, G)"
        ),
    )
    # Address related fields
    address = models.ForeignKey(
        Address,
        blank=True,
        null=True,
        on_delete=models.RESTRICT,
        related_name="address_properties",
        help_text=_("The physical address where the property is located."),
    )
    street_name = models.CharField(
        max_length=255,
        help_text=_(
            dedent(
                """The name of the street where the property is located.
                For example: 'Åfløjen'."""
            )
        ),
    )
    street_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text=_(
            dedent(
                """The house or building number on the street.
                Supports formats like '40', '12A', or '13-15'."""
            )
        ),
    )
    postal_code = models.CharField(
        max_length=20,
        help_text=_("The postal code for the property's location, e.g., '8000'."),
    )
    city = models.CharField(
        max_length=255,
        help_text=_("The city or town native name where the property is located."),
    )
    region = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_(
            dedent(
                """The administrative region or municipality of the property.
                This can be useful for broader geographical filtering."""
            )
        ),
    )
    country_code = models.CharField(
        max_length=2,
        help_text=_(
            dedent(
                """The ISO 3166-1 Alpha-2 country code (e.g., 'DK' for
                Denmark). Used for filtering and international support."""
            )
        ),
    )

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")
        indexes = [
            # Compound indexes for common filters
            models.Index(fields=["country_code", "status", "city"]),
            models.Index(fields=["country_code", "status", "property_type"]),
            models.Index(fields=["country_code", "status", "street_name"]),
            models.Index(fields=["country_code", "status", "price"]),
            models.Index(fields=["country_code", "status", "area"]),
            models.Index(fields=["country_code", "status", "postal_code"]),
            models.Index(fields=["country_code", "status", "total_rooms"]),
            # Support sorting if needed
            models.Index(fields=["country_code", "status", "created_at"]),
            models.Index(fields=["country_code", "status", "construction_year"]),
        ]

    def __str__(self) -> str:
        return _(
            "Property (Rooms: {total_rooms}, Price: {price} {currency}, Area: {area} sqm)"
        ).format(
            total_rooms=self.total_rooms or "N/A",
            price=self.price or "N/A",
            currency=self.price_currency or "",
            area=self.area or "N/A",
        )
