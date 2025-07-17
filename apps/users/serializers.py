import re
from typing import Any

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework.serializers import (
    BooleanField,
    CharField,
    EmailField,
    ModelSerializer,
)

from dj_rest_auth.registration.serializers import RegisterSerializer

from allauth.account.adapter import get_adapter

from .models import User


class AuthUserDetailsSerializer(ModelSerializer[User]):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "is_business_user",
            "is_company_admin",
            "agreed_to_terms",
            "phone_number",
            "is_verified",
            "subscription_status",
            "profile_photo",
        )
        read_only_fields = (
            "email",
            "username",
            "is_business_user",
            "is_company_admin",
            "is_verified",
            "subscription_status",
        )


class CustomRegisterSerializer(RegisterSerializer):  # type: ignore [misc]
    username = None  # disables handling of username if expected by base
    password1 = CharField(
        write_only=True,
        style={"input_type": "password"},
        help_text=_(
            "Password must be at least 8 characters long. "
            "It must not be entirely numeric, too common, "
            "or too similar to your personal information."
        ),
    )
    first_name = CharField(required=True, allow_blank=False)
    last_name = CharField(required=True, allow_blank=False)
    email = EmailField(required=True)
    agreed_to_terms = BooleanField(required=True)
    phone_number = CharField(required=False)
    is_business_user = BooleanField(required=False)
    is_company_admin = BooleanField(required=False)

    def validate_email(self, email: str) -> str:
        """
        Validate that the email is unique and correctly formatted.
        """
        email = get_adapter().clean_email(email)
        if not email.strip():
            raise ValidationError("Email is required.")
        elif email and User.objects.filter(email__iexact=email).exists():
            raise ValidationError(_("A user with that email already exists."))
        return email

    def validate_phone_number(self, phone_number: str) -> str:
        """
        Validate phone number format (optional but must be clean if provided).
        """
        PHONE_REGEX = r"^\+?[0-9]{7,15}$"  # basic international format
        if phone_number:
            if not re.match(PHONE_REGEX, phone_number):
                raise ValidationError(
                    _(
                        "Phone number must be digits, 7-15 long, "
                        "optionally starting with +."
                    )
                )
        return phone_number

    def get_cleaned_data(self) -> dict[str, Any]:
        data: dict[str, Any] = super().get_cleaned_data()
        data.update(
            {
                "first_name": self.validated_data.get("first_name", ""),
                "last_name": self.validated_data.get("last_name", ""),
                "phone_number": self.validated_data.get("phone_number", ""),
                "is_business_user": self.validated_data.get("is_business_user", False),
                "is_company_admin": self.validated_data.get("is_company_admin", False),
                "agreed_to_terms": self.validated_data.get("agreed_to_terms", False),
            }
        )
        return data
