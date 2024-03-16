from typing import Any

from rest_framework.serializers import (
    BaseSerializer,
    CharField,
    IntegerField,
)


class IdCodeListSerializer(BaseSerializer[Any]):
    """Serialize two field of types (integer, char)."""

    id = IntegerField
    code = CharField

    fields = (
        "id",
        "code",
    )

    def to_representation(self, obj: Any) -> Any:
        return obj
