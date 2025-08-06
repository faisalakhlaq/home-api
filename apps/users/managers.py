from __future__ import annotations

from typing import Any, TYPE_CHECKING

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from .models import User


class CustomUserManager(BaseUserManager["User"]):
    """
    Custom user manager where email is the unique identifier
    for authentication instead of username.
    """

    def create_user(
        self,
        email: str,
        password: str | None,
        first_name: str,
        last_name: str,
        **extra_fields: Any,
    ) -> "User":
        """
        Create and save a user with the given credentials.
        """
        if not email:
            raise ValueError(_("An email address is required."))
        if not first_name:
            raise ValueError(_("First name is required."))
        if not last_name:
            raise ValueError(_("Last name is required."))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        **extra_fields: Any,
    ) -> "User":
        """
        Create and save a superuser with the given credentials.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError(_("Superuser must have is_staff=True."))
        if not extra_fields.get("is_superuser"):
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
