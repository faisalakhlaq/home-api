import logging

from apps.locations.models import City, Country

from seed.city_data import danish_cities, macedonia_cities
from seed.countries_data import countries_data

logger = logging.getLogger(__name__)

# Seed countries
if not Country.objects.exists():  # type: ignore[attr-defined]
    country_objs = [Country(**data) for data in countries_data]
    country_list = Country.objects.bulk_create(country_objs)  # type: ignore[attr-defined]
    logger.info(f"Created a total of '{len(country_list)}' countries.")
else:
    logger.info("Countries already seeded.")

# Seed cities for North Macedonia
try:
    north_macedonia = Country.objects.get(name="North Macedonia", code="MK")  # type: ignore[attr-defined]
    macedonian_city_objs = [
        City(**data, country=north_macedonia) for data in macedonia_cities
    ]
    City.objects.bulk_create(macedonian_city_objs)  # type: ignore[attr-defined]
    logger.info(
        f"Created a total of '{len(macedonian_city_objs)}' cities for North Macedonia."
    )
except Country.DoesNotExist:
    logger.error("North Macedonia not found in the database.")

# Seed cities for Denmark
try:
    denmark = Country.objects.get(name="Denmark", code="DK")  # type: ignore[attr-defined]
    danish_city_objs = [City(**data, country=denmark) for data in danish_cities]
    City.objects.bulk_create(danish_city_objs)  # type: ignore[attr-defined]
    logger.info(f"Created a total of '{len(danish_city_objs)}' cities for Denmark.")
except Country.DoesNotExist:
    logger.error("Denmark not found in the database.")
