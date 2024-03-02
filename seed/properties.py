from typing import Any, Dict
import logging

from apps.core.models import Address
from apps.properties.models import Property

import random

logger = logging.getLogger(__name__)


# Generate test data for addresses
addresses_data = [
    {
        "street": "Street {}".format(i),
        "city": "City {}".format(i),
        "region": "Region {}".format(i),
        "postal_code": "12345",
        "country": "Country {}".format(i),
    }
    for i in range(1, 21)  # Generate 20 addresses
]


# Create Address objects
def create_address(address_data: Dict[str, Any]) -> Address | None:
    try:
        return Address.objects.create(**address_data)
    except Exception as ex:
        logger.exception(msg=str(ex))
        return None


addresses = list(map(create_address, addresses_data))
logger.info(f"Created Addresses = {addresses}")

# Generate test data for properties
test_data = [
    {
        "price": random.randint(
            100000, 1000000
        ),  # Random price between $100,000 and $1,000,000
        "price_currency": "USD",
        "area": random.randint(
            500, 5000
        ),  # Random area between 500 and 5000 square feet
        "total_area": random.randint(
            500, 5000
        ),  # Random total area between 500 and 5000 square feet
        "measured_area": random.randint(
            500, 5000
        ),  # Random measured area between 500 and 5000 square feet
        "total_rooms": random.randint(2, 10),  # Random total rooms between 2 and 10
        "toilets": random.randint(1, 5),  # Random number of toilets between 1 and 5
        "construction_year": random.randint(
            1980, 2020
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
            i - 1
        ],  # Associate the property with the corresponding address
    }
    for i in range(1, 21)  # Generate 20 records
]


# Create Property objects
def create_property(property_data: Dict[str, Any]) -> Property | None:
    try:
        return Property.objects.create(**property_data)
    except Exception as ex:
        logger.exception(msg=str(ex))
        return None


properties = list(map(create_property, test_data))
logger.info(f"Created properties = {properties}")
