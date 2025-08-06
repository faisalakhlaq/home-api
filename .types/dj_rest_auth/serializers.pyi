from typing import Dict, Any
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username: serializers.CharField | None
    password: serializers.CharField

    def get_auth_user(self, username: str, password: str) -> Any: ...
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]: ...
