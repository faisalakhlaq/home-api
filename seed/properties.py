from typing import Any, Dict
import logging

from apps.core.models import Address
from apps.properties.models import Property

import random

logger = logging.getLogger(__name__)


# Generate test data for addresses
addresses_data = [
    {
        "country": "North Macedonia",
        "city": "Skopje",
        "street": "Vasil Glavinov 9",
        "postal_code": "1000",
    },
    {
        "country": "North Macedonia",
        "city": "Bitola",
        "street": "Dame Gruev 25",
        "postal_code": "7000",
    },
    {
        "country": "North Macedonia",
        "city": "Kumanovo",
        "street": "Goce Delchev 14",
        "postal_code": "1300",
    },
    {
        "country": "North Macedonia",
        "city": "Prilep",
        "street": "Makedonska Brigada 7",
        "postal_code": "7500",
    },
    {
        "country": "North Macedonia",
        "city": "Tetovo",
        "street": "Kuzman Josifovski Pitu 33",
        "postal_code": "1200",
    },
    {
        "country": "North Macedonia",
        "city": "Ohrid",
        "street": "Kliment Ohridski 2",
        "postal_code": "6000",
    },
    {
        "country": "North Macedonia",
        "city": "Veles",
        "street": "Orce Nikolov 11",
        "postal_code": "1400",
    },
    {
        "country": "North Macedonia",
        "city": "Štip",
        "street": "Dimitar Vlahov 18",
        "postal_code": "2000",
    },
    {
        "country": "North Macedonia",
        "city": "Gostivar",
        "street": "11 Oktomvri 5",
        "postal_code": "1230",
    },
    {
        "country": "North Macedonia",
        "city": "Strumica",
        "street": "Partizanska bb",
        "postal_code": "2400",
    },
    {
        "country": "North Macedonia",
        "city": "Kočani",
        "street": "Rajko Zinzifov",
        "postal_code": "2300",
    },
    {
        "country": "North Macedonia",
        "city": "Kičevo",
        "street": "Maršal Tito",
        "postal_code": "6250",
    },
    {
        "country": "North Macedonia",
        "city": "Kratovo",
        "street": "Goce Delchev",
        "postal_code": "1360",
    },
    {
        "country": "North Macedonia",
        "city": "Delčevo",
        "street": "Ilindenska",
        "postal_code": "2320",
    },
    {
        "country": "North Macedonia",
        "city": "Struga",
        "street": "Kej Boris Kidrič",
        "postal_code": "6330",
    },
    {
        "country": "North Macedonia",
        "city": "Radoviš",
        "street": "Rajko Zinzifov",
        "postal_code": "2420",
    },
    {
        "country": "North Macedonia",
        "city": "Kavadarci",
        "street": "Goce Delchev",
        "postal_code": "1430",
    },
    {
        "country": "North Macedonia",
        "city": "Gevgelija",
        "street": "Goce Delchev",
        "postal_code": "1480",
    },
    {
        "country": "North Macedonia",
        "city": "Negotino",
        "street": "Goce Delchev",
        "postal_code": "1440",
    },
    {
        "country": "North Macedonia",
        "city": "Kriva alanka",
        "street": "Jane Sandanski",
        "postal_code": "1330",
    },
    {
        "country": "North Macedonia",
        "city": "Debar",
        "street": "Marshal Tito",
        "postal_code": "1250",
    },
    {
        "country": "North Macedonia",
        "city": "Vinica",
        "street": "Goce Delchev",
        "postal_code": "2310",
    },
    {
        "country": "North Macedonia",
        "city": "Resen",
        "street": "Marshal Tito",
        "postal_code": "7310",
    },
    {
        "country": "North Macedonia",
        "city": "Berovo",
        "street": "Marsal Tito",
        "postal_code": "2330",
    },
    {
        "country": "North Macedonia",
        "city": "Sveti ikole",
        "street": "Goce Delcev",
        "postal_code": "2220",
    },
    {
        "country": "North Macedonia",
        "city": "Probistip",
        "street": "Boris Kidrič",
        "postal_code": "2220",
    },
    {
        "country": "North Macedonia",
        "city": "Kicevo",
        "street": "Marsal Tito",
        "postal_code": "6250",
    },
    {
        "country": "North Macedonia",
        "city": "Demir apija",
        "street": "Goce Delčev",
        "postal_code": "1441",
    },
    {
        "country": "North Macedonia",
        "city": "Makedonski rod",
        "street": "Krste Misirkov",
        "postal_code": "6530",
    },
    {
        "country": "North Macedonia",
        "city": "Bogdanci",
        "street": "Marsal Tito",
        "postal_code": "1480",
    },
    {
        "country": "North Macedonia",
        "city": "Valandovo",
        "street": "Goce Delčev",
        "postal_code": "1470",
    },
    {
        "country": "North Macedonia",
        "city": "Dojran",
        "street": "Boris Kidrič",
        "postal_code": "1487",
    },
    {
        "country": "North Macedonia",
        "city": "Krushevo",
        "street": "Marshal Tito",
        "postal_code": "7550",
    },
    {
        "country": "North Macedonia",
        "city": "Demir isar",
        "street": "11 Oktomvri",
        "postal_code": "7315",
    },
    {
        "country": "North Macedonia",
        "city": "Bogovinje",
        "street": "Goce Delčev",
        "postal_code": "1221",
    },
    {
        "country": "North Macedonia",
        "city": "Češinovo-bleševo",
        "street": "Jane Sandanski",
        "postal_code": "2340",
    },
    {
        "country": "North Macedonia",
        "city": "Čaška",
        "street": "Goce Delčev",
        "postal_code": "1332",
    },
]


# Create Address objects
def create_address(address_data: Dict[str, Any]) -> Address | None:
    try:
        return Address.objects.create(**address_data)
    except Exception as ex:
        logger.exception(msg=str(ex))
        return None


addresses = list(map(create_address, addresses_data))
# logger.info(f"Created Addresses = {addresses}")

# Generate test data for properties
test_data = [
    {
        "price": random.randint(
            100000, 1000000
        ),  # Random price between $100,000 and $1,000,000
        "price_currency": "USD",
        "area": random.randint(50, 500),  # Random area between 500 and 5000 square feet
        "total_area": random.randint(
            50, 500
        ),  # Random total area between 500 and 5000 square feet
        "measured_area": random.randint(
            50, 500
        ),  # Random measured area between 500 and 5000 square feet
        "total_rooms": random.randint(2, 10),  # Random total rooms between 2 and 10
        "toilets": random.randint(1, 5),  # Random number of toilets between 1 and 5
        "construction_year": random.randint(
            1900, 2024
        ),  # Random construction year between 1980 and 2020
        "renovation_year": random.randint(
            1980, 2020
        ),  # Random renovation year between 1980 and 2020
        "total_floors": random.randint(1, 5),  # Random total floors between 1 and 5
        "heating": random.choice(
            ["Gas", "Electric", "Oil", "None"]
        ),  # Random heating type
        "outer_walls": random.choice(
            ["Brick", "Wood", "Stone", "Stucco"]
        ),  # Random outer walls type
        "roof_type": random.choice(
            ["Flat", "Pitched", "Gable", "Hip"]
        ),  # Random roof type
        "address": addresses[
            i
        ],  # Associate the property with the corresponding address
    }
    for i in range(0, 37)  # Generate 40 records
]


# Create Property objects
def create_property(property_data: Dict[str, Any]) -> Property | None:
    try:
        return Property.objects.create(**property_data)
    except Exception as ex:
        logger.exception(msg=str(ex))
        return None


properties = list(map(create_property, test_data))
# logger.info(f"Created properties = {properties}")
