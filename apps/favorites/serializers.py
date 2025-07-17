from rest_framework import serializers

from apps.properties.serializers import PropertySerializer
from apps.properties.models import Property

from .models import UserFavoriteProperty


class UserFavoritePropertySerializer(serializers.ModelSerializer[UserFavoriteProperty]):
    # For GET requests (listing favorites), we want to show property details
    property = PropertySerializer(read_only=True)

    # For POST requests (adding a favorite), we expect a property_id
    # Using PrimaryKeyRelatedField for write-only property ID input
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(), source="property", write_only=True
    )

    class Meta:
        model = UserFavoriteProperty
        fields = ["id", "user", "property", "property_id", "created_at", "updated_at"]
        read_only_fields = ["user", "created_at", "updated_at"]
