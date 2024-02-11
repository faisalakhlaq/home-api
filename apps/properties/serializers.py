from apps.properties.models import Property

from rest_framework.serializers import ModelSerializer


class PropertySerialzier(ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"
