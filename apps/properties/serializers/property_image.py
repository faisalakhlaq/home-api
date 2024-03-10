from rest_framework.serializers import ModelSerializer

from apps.properties.models import PropertyImage


class PropertyImageSerializer(ModelSerializer[PropertyImage]):
    class Meta:
        model = PropertyImage
        fields = "__all__"


class PropertyImageDetailSerializer(ModelSerializer[PropertyImage]):
    class Meta:
        model = PropertyImage
        fields = ["id", "title", "description", "is_primary", "image"]


class PropertyPrimaryImageSerialzier(ModelSerializer[PropertyImage]):
    class Meta:
        model = PropertyImage
        fields = ("image",)
