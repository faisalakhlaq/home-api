from rest_framework.serializers import ModelSerializer

from apps.core.models import Address


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
