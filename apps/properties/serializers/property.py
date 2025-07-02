from typing import Any, Dict

from django.db import transaction

from rest_framework.serializers import BooleanField, CharField, ModelSerializer

from apps.properties.models import Property, PropertyImage
from apps.core.serializers.address import (
    AddressSerializer,
    PropertyListAddressSerializer,
)

from .property_image import (
    PropertyImageDetailSerializer,
    PropertyImageSerializer,
    PropertyPrimaryImageSerialzier,
)


class PropertySerializer(ModelSerializer[Property]):
    address = AddressSerializer()
    property_images = PropertyImageDetailSerializer(many=True, required=False)

    class Meta:
        model = Property
        fields = "__all__"

    @transaction.atomic()
    def create(self, validated_data: Dict[str, Any]) -> Property:
        address_data = validated_data.pop("address")
        property_images_data = validated_data.pop("property_images", [])

        address_ser = AddressSerializer(data=address_data)
        if address_ser.is_valid(raise_exception=True):
            address_instance = address_ser.save()
            validated_data["address"] = address_instance

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


class PropertyDetailSerializer(ModelSerializer[Property]):
    type = CharField(source="type.name", default="", read_only=True)
    address = AddressSerializer()
    property_images = PropertyImageSerializer(many=True, required=False)

    class Meta:
        model = Property
        fields = "__all__"


class PropertyListSerializer(ModelSerializer[Property]):
    type = CharField(source="type.name", default="", read_only=True)
    address = PropertyListAddressSerializer(read_only=True)
    image = PropertyPrimaryImageSerialzier(read_only=True)
    favorite = BooleanField(source="is_favorite", default=False, read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "type",
            "description",
            "created_at",
            "price",
            "price_currency",
            "address",
            "image",
            "favorite",
        ]
