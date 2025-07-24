from typing import Any, Dict, List
import logging
from itertools import groupby

from django.db import transaction
from django.db.utils import IntegrityError
from django.utils.text import slugify

from apps.locations.models import City, Country

from seed.city_data import danish_cities, macedonia_cities
from seed.countries_data import countries_data

logger = logging.getLogger(__name__)


def seed_cities(city_data_list: List[Dict[str, Any]], country: Country) -> None:
    """
    Seed cities with proper slug handling using Django's slugify.
    Handles duplicates within the same country automatically.

    Args:
        city_data_list: List of dictionaries containing city data
        country: Country instance to associate cities with

    Returns:
        None
    """
    cities: List[City] = []

    # Sort and group by city name to handle duplicates
    city_data_list.sort(key=lambda x: str(x["name"]))
    grouped_cities = groupby(city_data_list, key=lambda x: str(x["name"]))

    for city_name, group in grouped_cities:
        group_list = list(group)
        base_slug = (
            f"{slugify(city_name)}-{country.code.lower()}"  # Using Django's slugify
        )

        for i, city_data in enumerate(group_list):
            city = City(
                name=str(city_data["name"]),
                country=country,
                region=city_data.get("region"),
                latitude=city_data.get("latitude"),
                longitude=city_data.get("longitude"),
                slug=f"{base_slug}-{i}" if i > 0 else base_slug,
            )
            cities.append(city)

    # Batch create with 500 cities at a time
    batch_size = 500
    with transaction.atomic():
        for i in range(0, len(cities), batch_size):
            to = i + batch_size
            try:
                City.objects.bulk_create(cities[i:to])  # No E203 violation
            except IntegrityError as ie:
                logger.exception(
                    msg=f"IntegrityError while creating cities for {country.name}",
                    exc_info=ie,
                )
    logger.info(f"Seeded {len(cities)} cities for {country.name}")


# Seed countries
if not Country.objects.exists():
    country_objs = [Country(**data) for data in countries_data]
    try:
        country_list = Country.objects.bulk_create(country_objs)
        logger.info(f"Created a total of '{len(country_list)}' countries.")
    except IntegrityError as ie:
        logger.exception(msg="IntegrityError while creating countries", exc_info=ie)
else:
    logger.info("Countries already seeded.")


# Seed cities for North Macedonia
try:
    north_macedonia = Country.objects.get(name="North Macedonia", code="MK")
    seed_cities(macedonia_cities, north_macedonia)
except Country.DoesNotExist:
    logger.error("Country not found")


# Seed cities for Denmark
try:
    denmark = Country.objects.get(name="Denmark", code="DK")
    seed_cities(danish_cities, denmark)
except Country.DoesNotExist:
    logger.error("Country not found")
