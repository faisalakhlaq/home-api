import logging
from random import choice
from typing import Any, Dict, Optional

from django.contrib.contenttypes.models import ContentType

from apps.core.models import Genre

logger = logging.getLogger(__name__)


def create_genre(genre: Dict[str, Any]) -> Optional[Genre]:
    try:
        return Genre.objects.create(**genre)
    except Exception as ex:
        logger.exception(msg=f"Seed: Unable to create Genre={ex}.")
        return None


property_genre_data = [
    {
        "name": "Single-family detached home",
        "description": """Stand-alone houses that are not attached to any other
        structures.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Apartment",
        "description": """Multi-unit buildings with separate units for
        individual households, often rented out by landlords.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Condominium",
        "description": """(Condos) Privately owned units within a larger
        building or complex, with shared common areas and amenities.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Townhouse",
        "description": """(Terraced houses) Attached homes that share walls
        with neighboring units, typically arranged in a row or block.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Duplex",
        "description": """Buildings divided into two separate living units,
        often with each unit having its own entrance.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Triplexe",
        "description": """Buildings divided into three separate living units,
        often with each unit having its own entrance.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Co-operative housing",
        "description": """(Co-ops) Residents own shares in a corporation that
        owns the entire property, rather than owning individual units.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Farmhouse",
        "description": """Homes located on rural agricultural land, often with
        space for farming or livestock.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Mansion",
        "description": """Large, luxurious homes typically associated with
        wealth and prestige.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Ground",
        "description": """Land for constructing a house.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Boat house",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Recreational residence",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Country property",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
]

list(map(create_genre, property_genre_data))

def create_test_genre()->Genre:
    return create_genre(choice(property_genre_data))