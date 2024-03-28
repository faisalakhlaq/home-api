import logging
from random import choice
from typing import Any, Dict, Optional

from django.contrib.contenttypes.models import ContentType

from apps.core.models import Status

logger = logging.getLogger(__name__)


def create_status(status: Dict[str, Any]) -> Optional[Status]:
    try:
        return Status.objects.create(**status)
    except Exception as ex:
        logger.exception(msg=f"Seed: Unable to create status={ex}.")
        return None


property_status_data = [
    {
        "name": "Active",
        "description": """The property is actively available for sale or rent,
        and interested buyers or renters can make inquiries or schedule viewings.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Pending",
        "description": """The property has an accepted offer or is under
        contract, but the sale has not yet been completed. This status
        indicates that the sale is in progress, but certain conditions
        may need to be met before it is finalized.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Under contract",
        "description": """Similar to pending, this status indicates that the
        property has an accepted offer and is under a contract between the
        buyer and seller. However, specific contingencies may still need to be
        fulfilled before sale completion.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Sold",
        "description": """The property has been successfully sold, and the sale
        has been finalized. It is no longer available for purchase or rent.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Off market",
        "description": """The property listing has been removed from active
        marketing and is no longer available for sale or rent. This status may
        indicate that the property has been withdrawn temporarily or
        permanently from the market.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Expired",
        "description": """The listing agreement for the property has expired
        without the property being sold or rented. It is no longer actively
        marketed, but it may be relisted in the future with a new listing
        agreement.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Withdrawn",
        "description": """The property listing has been temporarily withdrawn
        from the market by the seller or their agent. It may be relisted at a
        later time.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Coming soon",
        "description": """A status indicating that the property will be
        available for sale or rent in the near future, but it is not yet
        actively marketed. It may be used to generate interest or anticipation
        before the property is officially listed.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Auction",
        "description": """The property is being sold through an auction
        process, where interested buyers can bid on the property until a
        predetermined deadline.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
    {
        "name": "Leased",
        "description": """The property has been successfully rented out to a
        tenant, and a lease agreement is in place. It is no longer available
        for rent.""",
        "model": ContentType.objects.get(app_label="properties", model="property"),
        "sorting_order": 1,
        "active": True,
    },
]

list(map(create_status, property_status_data))

def create_test_status()->Status:
    return create_status(choice(property_status_data))