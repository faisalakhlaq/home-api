from typing import Any, Dict

from django.db import transaction

from rest_framework.serializers import BooleanField, ModelSerializer

from apps.properties.models import Property, PropertyImage

from .property_image import (
    PropertyImageSerializer,
    PropertyPrimaryImageSerialzier,
)


class PropertySerializer(ModelSerializer[Property]):
    property_images = PropertyImageSerializer(many=True, required=False)

    class Meta:
        model = Property
        fields = "__all__"

    @transaction.atomic()
    def create(self, validated_data: Dict[str, Any]) -> Property:
        property_images_data = validated_data.pop("property_images", [])

        validated_data["owner"] = (
            self.context.get("request").user  # type: ignore
            if self.context.get("request")
            else None
        )

        property_instance = super(PropertySerializer, self).create(validated_data)

        if property_images_data:
            image_serializer = PropertyImageSerializer(
                data=[
                    {**image, "property": property_instance.id}
                    for image in property_images_data
                ],
                many=True,
            )
            if image_serializer.is_valid(raise_exception=True):
                property_images = [
                    PropertyImage(**image) for image in image_serializer.validated_data
                ]
                PropertyImage.objects.bulk_create(property_images)

        return property_instance


class PropertyListSerializer(ModelSerializer[Property]):
    image = PropertyPrimaryImageSerialzier(read_only=True)
    favorite = BooleanField(source="is_favorite", default=False, read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "property_type",
            "description",
            "created_at",
            "price",
            "price_currency",
            "total_rooms",
            "area",
            "energy_class",
            "street_name",
            "street_number",
            "postal_code",
            "city",
            "image",
            "favorite",
        ]
