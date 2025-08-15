from rest_framework.serializers import ModelSerializer

from apps.properties.models import PropertyImage


class PropertyImageSerializer(ModelSerializer[PropertyImage]):
    class Meta:
        model = PropertyImage
        fields = "__all__"
