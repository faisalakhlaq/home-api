from django.db import models
from django.contrib.auth import get_user_model

from apps.properties.models import Property

User = get_user_model()


class UserFavoriteProperty(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorite_properties"
    )
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="favorite_user"
    )

    class Meta:
        unique_together = ("user", "property")
