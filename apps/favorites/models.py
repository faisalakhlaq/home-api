from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _  # Import for translation

from apps.core.models import TimeTracking
from apps.properties.models import Property

User = get_user_model()


class UserFavoriteProperty(TimeTracking):
    """
    Represents a user's favorite property.

    This model links a specific user to a property they have marked as a favorite.
    It ensures that a user can only favorite a particular property once.

    Attributes:
        user (ForeignKey): The user who marked the property as a favorite.
        property (ForeignKey): The property that has been favorited by the user.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite_properties",
        help_text=_("The user who marked this property as a favorite."),
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="favorite_user",
        help_text=_("The property that has been favorited by the user."),
    )

    class Meta:
        unique_together = ("user", "property")
        verbose_name = _("User Favorite Property")
        verbose_name_plural = _("User Favorite Properties")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """
        Returns a string representation of the user favorite property instance.
        """
        property_title = f"{self.property.price} {self.property.price_currency}"
        return _("{username} favorited {property}").format(
            username=self.user.username, property=property_title
        )
