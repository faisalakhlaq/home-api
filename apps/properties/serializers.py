from apps.properties.models import Property, PropertyImage

from rest_framework.serializers import ModelSerializer

from apps.core.models import Address


class PropertySerialzier(ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class PropertyImageSerializer(ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['title', 'description', 'is_primary', 'image']

class PropertySerializer(ModelSerializer):
    address = AddressSerializer()
    property_images = PropertyImageSerializer(many=True)

    class Meta:
        model = Property
        fields = '__all__'

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        property_images_data = validated_data.pop('property_images')

        address_ser = AddressSerializer(data=address_data)
        if address_ser.is_valid(raise_exception=True):
            address_instance = address_ser.save()
            validated_data['address'] = address_instance

        property_instance = super(PropertySerializer, self).create(validated_data)

        # Assign property_instance to each PropertyImage instance
        for image_data in property_images_data:
            image_data['property'] = property_instance.id

        # Serialize and save all PropertyImage instances
        image_serializer = PropertyImageSerializer(data=property_images_data, many=True)
        if image_serializer.is_valid():
            property_images = [PropertyImage(**image) for image in image_serializer.validated_data]
            PropertyImage.objects.bulk_create(property_images)

        return property_instance
