from typing import Any, Dict

from django.utils.translation import gettext_lazy as _

from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    ValidationError,
)

from apps.properties.serializers import PropertyListSerializer
from apps.properties.models import Property

from .models import UserFavoriteProperty


class WritableUserFavoritePropertySerializer(ModelSerializer[UserFavoriteProperty]):
    # For POST requests (adding a favorite), we expect a property_id
    # Using PrimaryKeyRelatedField for write-only property ID input
    property_id = PrimaryKeyRelatedField(
        queryset=Property.objects.all(), source="property", write_only=True
    )

    class Meta:
        model = UserFavoriteProperty
        fields = ["id", "user", "property_id", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """Check for duplicate favorites."""
        request = self.context.get("request")
        if not request or not hasattr(request, "user") or request.user.is_anonymous:
            raise ValidationError(
                {"user": _("Authentication is required to favorite properties.")}
            )

        user = request.user
        property_instance = attrs["property"]

        if UserFavoriteProperty.objects.filter(
            user=user, property=property_instance
        ).exists():
            raise ValidationError(
                {"property_id": _("This property is already in your favorites.")}
            )

        return attrs

    def create(self, validated_data: Dict[str, Any]) -> UserFavoriteProperty:
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class UserFavoritePropertyListSerializer(ModelSerializer[UserFavoriteProperty]):
    property = PropertyListSerializer(read_only=True)

    class Meta:
        model = UserFavoriteProperty
        fields = ["id", "user", "property", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]
