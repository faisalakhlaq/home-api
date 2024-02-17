from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from apps.properties.models import Property
from apps.properties.serializers import PropertySerialzier


class PropertyViewSet(ModelViewSet):
    """CRUD API for properties.

    POST Payload:
    {
        "price": 10,
        "price_currency": "EUR",
        "area": 10,
        "total_area": 12,
        "measured_area": 11,
        "total_rooms": 1,
        "toilets": 1,
        "construction_year": 1900,
        "renovation_year": 1950,
        "total_floors": 1,
        "heating": "Central heating with one heating unit.",
        "outer_walls": "Brick",
        "roof_type": "Tile",
        "address": "",
    }
    Address payload within properties POST:
    {
        "street": "Some street, building number, floor 1"
        "city": "City name"
        "region": "region name"
        "postal_code": "12345"
        "country": "Country Name"
    }
    Image payload within properties POST:
    {
        {
            "title": "Optional",
            "description": "Optional",
            "is_primary": false,
            "image": File,
        }
        ............
        ............
    }
    """

    permission_classes = [AllowAny]
    serializer_class = PropertySerialzier
    queryset = Property.objects.all()
