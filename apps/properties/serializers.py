from typing import Any, Dict

from django.db import transaction

from rest_framework.serializers import ModelSerializer

from apps.core.models import Address
from apps.properties.models import Property, PropertyImage


class AddressSerializer(ModelSerializer[Address]):
    class Meta:
        model = Address
        fields = "__all__"


class PropertyListAddressSerializer(ModelSerializer[Address]):
    class Meta:
        model = Address
        fields = [
            "postal_code",
            "street",
            "city",
        ]


class PropertyImageSerializer(ModelSerializer[PropertyImage]):
    class Meta:
        model = PropertyImage
        fields = ["title", "description", "is_primary", "image"]


class PropertyPrimaryImageSerialzier(ModelSerializer[PropertyImage]):
    class Meta:
        model = PropertyImage
        fields = ("image",)


class PropertySerializer(ModelSerializer[Property]):
    address = AddressSerializer()
    property_images = PropertyImageSerializer(many=True, required=False)

    class Meta:
        model = Property
        fields = "__all__"

    @transaction.atomic()
    def create(self, validated_data: Dict[str, Any]) -> Property:
        address_data = validated_data.pop("address")
        property_images_data = validated_data.pop("property_images")

        address_ser = AddressSerializer(data=address_data)
        if address_ser.is_valid(raise_exception=True):
            address_instance = address_ser.save()
            validated_data["address"] = address_instance

        property_instance = super(PropertySerializer, self).create(validated_data)

        # Assign property_instance to each PropertyImage instance
        for image_data in property_images_data:
            image_data["property"] = property_instance.id

        # Serialize and save all PropertyImage instances
        image_serializer = PropertyImageSerializer(data=property_images_data, many=True)
        if image_serializer.is_valid():
            property_images = [
                PropertyImage(**image) for image in image_serializer.validated_data
            ]
            PropertyImage.objects.bulk_create(property_images)

        return property_instance


class PropertyListSerializer(ModelSerializer[Property]):
    address = PropertyListAddressSerializer(read_only=True)
    images = PropertyPrimaryImageSerialzier(read_only=True)

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
            "images",
        ]
