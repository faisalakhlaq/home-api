from typing import Any

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.managers import CustomUserManager


class User(AbstractUser):
    """Custom user model using email as username field.

    The purpose of the custom user model is to remove the username field and
    accommodate the business users.

    A company registered as a business can add its employees as users. The
    corresponding users will then inherit all the permissions that the company
    gives them. A company must have one or more admin users, who are
    responsible for adding and deleting company users and assigning them
    permissions.

    ## Fields
    * is_business_user (bool) Is the user related to a business customer.
    * is_company_admin (bool) Admin user for the company.

    #### Inherited fields (from AbstractUser, some may be overridden)
    1. _state (ModelState) Used to preserve the state of the user.
    2. id (int) Unique ID for each user.
    3. password (string): Encrypted password for the user.
    4. last_login (datetime): Date and time when user last logged in.
    5. is_superuser (bool): True if the user is superuser, else false.
    6. first_name (string): First name of the user.
    7. last_name (string): Last name of the user.
    8. email (email): Email ID of the user.
    9. is_staff (bool): True if the user is a staff member, else false.
    10. is_active (bool): Is profile active.
    11. date_joined (datetime)
    """

    # silence mypy for the redefinition
    username = models.CharField(  # type: ignore[assignment]
        _("username"),
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        help_text=_(
            "Optional public username. Not used for login. " "Must be unique if set."
        ),
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        help_text=_("Required. Used as the login identifier."),
    )
    first_name = models.CharField(
        _("first name"),
        max_length=150,
        blank=True,
        help_text=_("User’s given name."),
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=True,
        help_text=_("User’s family name."),
    )
    full_name = models.CharField(
        _("full name"),
        max_length=301,
        blank=True,
        help_text=_("Auto-generated full name from first and last name."),
    )
    is_business_user = models.BooleanField(
        default=False,
        help_text=_(
            "Indicates if user is part of a business customer account. "
            "Businesses can add multiple users."
        ),
    )
    is_company_admin = models.BooleanField(
        default=False,
        help_text=_(
            "Designates whether the user is an admin of the company. "
            "Admins manage users and settings."
        ),
    )
    phone_number = models.CharField(
        _("phone number"),
        max_length=20,
        blank=True,
        null=True,
        help_text=_("Optional contact number."),
    )
    profile_photo = models.ImageField(
        _("profile photo"),
        upload_to="profiles/",
        blank=True,
        null=True,
        help_text=_("Optional profile image."),
    )
    is_verified = models.BooleanField(
        default=False,
        help_text=_("Has the account been verified (e.g., KYC or email)?"),
    )
    agreed_to_terms = models.BooleanField(
        default=False,
        help_text=_("Indicates whether the user agreed to the terms of use."),
    )
    subscription_status = models.CharField(
        max_length=20,
        choices=[("active", _("Active")), ("inactive", _("Inactive"))],
        default="inactive",
        help_text=_("Indicates current subscription status."),
    )
    stripe_customer_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Stripe customer ID used for payments."),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]  # These are prompted for createsuperuser

    objects = CustomUserManager()  # type: ignore[misc, assignment]

    def __str__(self) -> str:
        """Returns the email address as a string representation."""
        return self.email

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Saves the user and updates the full_name field."""
        self.full_name = f"{self.first_name} {self.last_name}".strip()
        super().save(*args, **kwargs)
