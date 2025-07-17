from typing import Any

from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField, CharField


class User(AbstractUser):
    """Custom user model.

    The purpose of the custom user model is to accomodate the business users.
    A company registered as a business can add their employees as a user. The
    corresponding users will then inherit all the permissions that the company
    gives them. A company must have an (can have one or more) admin user, who
    is responsible to adding and deleting company users and assign them
    permissions.

    Fields
    ------
    * is_business_user (bool) Is the user related to a business customer.
    * is_company_admin (bool) Admin user for the company.

    Inherited fields
    ----------------
    1. _state (ModelState) It is used to preserve the state of the user.
    2. id (int)	Unique ID for each user.
    3. password (string): Encrypted password for the user.
    4. last_login (datetime): Date and time when user logged in last time.
    5. is_superuser (bool): True if the user is superuser, otherwise false.
    6. username (string): Unique username for the user.
    7. first_name (string): First name of the user.
    8. last_name (string): Last name of the user.
    9. email (email): Email ID of the user.
    10.	is_staff (bool): Set true if the user is a staff member, else false.
    11.	is_active (bool): Is profile active.
    12.	date_joined (datetime)
    """

    is_business_user = BooleanField(
        default=False,
        help_text="""Is the user related to a business customer. A company
        registered as a customer may have many users.""",
    )
    is_company_admin = BooleanField(
        default=False,
        help_text="""Every company registerd as a business customer requires
        an admin. Only the company admin can add users to the company.""",
    )
    full_name = CharField(max_length=255, blank=True)

    @property
    def name(self) -> str:
        name = f"{self.first_name} {self.last_name}".strip()
        return name or self.username

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_name = f"{self.first_name} {self.last_name}".strip() or self.username
        super().save(*args, **kwargs)
