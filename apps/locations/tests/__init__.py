from .country_model_tests import TestCountryModel
from .city_model_tests import TestCityModel
from .city_translation_model_tests import TestCityTranslation
from .location_model_tests import TestLocationModel
from .address_model_tests import TestAddressModel
from .signals_tests import TestGenerateSlug

__all__ = [
    "TestCountryModel",
    "TestCityModel",
    "TestCityTranslation",
    "TestLocationModel",
    "TestAddressModel",
    "TestGenerateSlug",
]
