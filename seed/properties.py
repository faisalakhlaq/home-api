from typing import Any, Dict
import logging

from apps.properties.models import Property

import random

logger = logging.getLogger(__name__)


# Generate test data for addresses
address_data = [
    {
        "country_code": "MK",
        "city": "Skopje",
        "street_name": "Vasil Glavinov 9",
        "postal_code": "1000",
    },
    {
        "country_code": "MK",
        "city": "Bitola",
        "street_name": "Dame Gruev 25",
        "postal_code": "7000",
    },
    {
        "country_code": "MK",
        "city": "Kumanovo",
        "street_name": "Goce Delchev 14",
        "postal_code": "1300",
    },
    {
        "country_code": "MK",
        "city": "Prilep",
        "street_name": "Makedonska Brigada 7",
        "postal_code": "7500",
    },
    {
        "country_code": "MK",
        "city": "Tetovo",
        "street_name": "Kuzman Josifovski Pitu 33",
        "postal_code": "1200",
    },
    {
        "country_code": "MK",
        "city": "Ohrid",
        "street_name": "Kliment Ohridski 2",
        "postal_code": "6000",
    },
    {
        "country_code": "MK",
        "city": "Veles",
        "street_name": "Orce Nikolov 11",
        "postal_code": "1400",
    },
    {
        "country_code": "MK",
        "city": "Štip",
        "street_name": "Dimitar Vlahov 18",
        "postal_code": "2000",
    },
    {
        "country_code": "MK",
        "city": "Gostivar",
        "street_name": "11 Oktomvri 5",
        "postal_code": "1230",
    },
    {
        "country_code": "MK",
        "city": "Strumica",
        "street_name": "Partizanska bb",
        "postal_code": "2400",
    },
    {
        "country_code": "MK",
        "city": "Kočani",
        "street_name": "Rajko Zinzifov",
        "postal_code": "2300",
    },
    {
        "country_code": "MK",
        "city": "Kičevo",
        "street_name": "Maršal Tito",
        "postal_code": "6250",
    },
    {
        "country_code": "MK",
        "city": "Kratovo",
        "street_name": "Goce Delchev",
        "postal_code": "1360",
    },
    {
        "country_code": "MK",
        "city": "Delčevo",
        "street_name": "Ilindenska",
        "postal_code": "2320",
    },
    {
        "country_code": "MK",
        "city": "Struga",
        "street_name": "Kej Boris Kidrič",
        "postal_code": "6330",
    },
    {
        "country_code": "MK",
        "city": "Radoviš",
        "street_name": "Rajko Zinzifov",
        "postal_code": "2420",
    },
    {
        "country_code": "MK",
        "city": "Kavadarci",
        "street_name": "Goce Delchev",
        "postal_code": "1430",
    },
    {
        "country_code": "MK",
        "city": "Gevgelija",
        "street_name": "Goce Delchev",
        "postal_code": "1480",
    },
    {
        "country_code": "MK",
        "city": "Negotino",
        "street_name": "Goce Delchev",
        "postal_code": "1440",
    },
    {
        "country_code": "MK",
        "city": "Kriva alanka",
        "street_name": "Jane Sandanski",
        "postal_code": "1330",
    },
    {
        "country_code": "MK",
        "city": "Debar",
        "street_name": "Marshal Tito",
        "postal_code": "1250",
    },
    {
        "country_code": "MK",
        "city": "Vinica",
        "street_name": "Goce Delchev",
        "postal_code": "2310",
    },
    {
        "country_code": "MK",
        "city": "Resen",
        "street_name": "Marshal Tito",
        "postal_code": "7310",
    },
    {
        "country_code": "MK",
        "city": "Berovo",
        "street_name": "Marsal Tito",
        "postal_code": "2330",
    },
    {
        "country_code": "MK",
        "city": "Sveti ikole",
        "street_name": "Goce Delcev",
        "postal_code": "2220",
    },
    {
        "country_code": "MK",
        "city": "Probistip",
        "street_name": "Boris Kidrič",
        "postal_code": "2220",
    },
    {
        "country_code": "MK",
        "city": "Kicevo",
        "street_name": "Marsal Tito",
        "postal_code": "6250",
    },
    {
        "country_code": "MK",
        "city": "Demir apija",
        "street_name": "Goce Delčev",
        "postal_code": "1441",
    },
    {
        "country_code": "MK",
        "city": "Makedonski rod",
        "street_name": "Krste Misirkov",
        "postal_code": "6530",
    },
    {
        "country_code": "MK",
        "city": "Bogdanci",
        "street_name": "Marsal Tito",
        "postal_code": "1480",
    },
    {
        "country_code": "MK",
        "city": "Valandovo",
        "street_name": "Goce Delčev",
        "postal_code": "1470",
    },
    {
        "country_code": "MK",
        "city": "Dojran",
        "street_name": "Boris Kidrič",
        "postal_code": "1487",
    },
    {
        "country_code": "MK",
        "city": "Krushevo",
        "street_name": "Marshal Tito",
        "postal_code": "7550",
    },
    {
        "country_code": "MK",
        "city": "Demir isar",
        "street_name": "11 Oktomvri",
        "postal_code": "7315",
    },
    {
        "country_code": "MK",
        "city": "Bogovinje",
        "street_name": "Goce Delčev",
        "postal_code": "1221",
    },
    {
        "country_code": "MK",
        "city": "Češinovo-bleševo",
        "street_name": "Jane Sandanski",
        "postal_code": "2340",
    },
    {
        "country_code": "MK",
        "city": "Čaška",
        "street_name": "Goce Delčev",
        "postal_code": "1332",
    },
]

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
    }
    for i in range(0, 37)  # Generate 40 records
]

for address, property in zip(address_data, test_data):
    property.update(**address)


# Create Property objects
def create_property(property_data: Dict[str, Any]) -> Property | None:
    try:
        return Property.objects.create(**property_data)
    except Exception as ex:
        logger.exception(msg=str(ex))
        return None


properties = list(map(create_property, test_data))
# logger.info(f"Created properties = {properties}")
