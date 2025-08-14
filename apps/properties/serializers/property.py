import re
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


class WritablePropertySerializer(ModelSerializer[Property]):
    class PropertyImageCreateSerializer(ModelSerializer[PropertyImage]):
        class Meta:
            model = PropertyImage
            fields = ("title", "description", "is_primary", "image")
            extra_kwargs = {"image": {"required": False}}

    property_images = PropertyImageCreateSerializer(many=True, required=False)

    class Meta:
        model = Property
        fields = "__all__"

    @transaction.atomic()
    def create(self, validated_data: Dict[str, Any]) -> Property:
        validated_data.pop("property_images", [])

        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["owner"] = request.user

        property_instance = Property.objects.create(**validated_data)

        # Manually reconstruct and create the PropertyImage instances
        if request and request.data and request.FILES:
            request_data = request.data
            request_files = request.FILES

            # Use a regex to find all image-related title fields
            # This list comprehension is now safe because we've checked that request_data is not None
            image_keys = [
                k
                for k in request_data.keys()
                if re.match(r"property_images\[\d+\]\.title", k)
            ]

            # Get the unique indices from the keys (e.g., [0], [1], etc.)
            indices = []
            for k in image_keys:
                match = re.search(r"\[(\d+)\]", k)
                if match:  # The mypy fix: check if a match was found
                    indices.append(match.group(1))

            unique_indices = sorted(list(set(indices)))

            for index in unique_indices:
                # Reconstruct a single image's data from the flat request data
                image_title_key = f"property_images[{index}].title"
                image_is_primary_key = f"property_images[{index}].is_primary"
                image_file_key = f"property_images[{index}].image"

                title = request_data.get(image_title_key, "")
                is_primary_str = request_data.get(image_is_primary_key, "false")
                is_primary = is_primary_str.lower() == "true"
                image_file = request_files.get(image_file_key)

                if image_file:
                    PropertyImage.objects.create(
                        property=property_instance,
                        title=title,
                        is_primary=is_primary,
                        image=image_file,
                    )

        return property_instance
