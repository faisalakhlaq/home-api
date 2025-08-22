# Standard library imports
import logging
from typing import Any, TYPE_CHECKING, Type, cast

from django.db.models import (
    Case,
    IntegerField,
    Prefetch,
    QuerySet,
    When,
)
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from apps.properties.models import PropertyImage
from apps.favorites.models import UserFavoriteProperty

from .serializers import (
    UserFavoritePropertyListSerializer,
    WritableUserFavoritePropertySerializer,
)

logger = logging.getLogger(__name__)
User = get_user_model()

# Define a type alias for static type checking
if TYPE_CHECKING:
    # This block is only for type checkers (Mypy, Pylance).
    from apps.users.models import User as CustomUserType  # noqa: I300
else:
    # At runtime, CustomUserType will simply refer to the obtained User model.
    CustomUserType = User


class UserFavoritePropertyViewSet(ModelViewSet[UserFavoriteProperty]):
    """
    ViewSet for managing user favorite properties.

    Provides actions to list, add, and remove properties from a user's favorites.
    """

    serializer_class = UserFavoritePropertyListSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserFavoriteProperty.objects.all()

    def get_queryset(self) -> QuerySet[UserFavoriteProperty]:
        """
        Returns the queryset of favorite properties for the authenticated user.
        """
        user = cast(CustomUserType, self.request.user)
        favorite_qs = (
            UserFavoriteProperty.objects.filter(user=user)
            .select_related("property")
            .order_by("created_at")
        )

        if self.action in ["list", "retrieve"]:
            image_queryset = PropertyImage.objects.order_by(
                Case(
                    When(is_primary=True, then=0),
                    default=1,
                    output_field=IntegerField(),
                ),
                "id",
            )
            favorite_qs = favorite_qs.prefetch_related(
                Prefetch(
                    "property__property_images",
                    queryset=image_queryset,
                    to_attr="prefetched_images",
                )
            )

        return favorite_qs

    def get_serializer_class(self) -> Type[ModelSerializer[UserFavoriteProperty]]:
        if self.action in ["list", "retrieve"]:
            return UserFavoritePropertyListSerializer
        else:
            return WritableUserFavoritePropertySerializer

    @extend_schema(
        summary=_("Add a property to user's favorites"),
        description=_(
            "Adds a specified property to the authenticated user's " "favorite list."
        ),
        request=WritableUserFavoritePropertySerializer,
        responses={
            HTTP_201_CREATED: OpenApiResponse(
                response=WritableUserFavoritePropertySerializer,
                description=_("Property successfully added to favorites."),
                examples=[
                    OpenApiExample(
                        name="Successful Favorite Addition",
                        value={
                            "id": 1,
                            "user": 1,
                            "created_at": "2025-01-01T12:00:00Z",
                            "updated_at": "2025-01-01T12:00:00Z",
                        },
                        response_only=True,
                    )
                ],
            ),
            HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description=_("Authentication credentials were not provided.")
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                description=_(
                    "Bad Request / Invalid Data. e.g., 'property_id' "
                    "is missing or invalid."
                )
            ),
            HTTP_409_CONFLICT: OpenApiResponse(
                description=_("Conflict: This property is already in " "favorites."),
                examples=[
                    OpenApiExample(
                        name="Duplicate Favorite Error",
                        value={
                            "detail": _("This property is already in " "favorites.")
                        },
                        response_only=True,
                    )
                ],
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description=_("Not Found: Property with given ID does not exist.")
            ),
        },
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handles POST requests to create a new favorite property entry.
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary=_("List user's favorite properties"),
        description=_(
            "Retrieves a list of all properties favorited by the " "authenticated user."
        ),
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handles GET requests to list favorite properties.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary=_("Remove a property from user's favorites"),
        description=_(
            "Removes a specific property from the authenticated "
            "user's favorite list by its favorite entry ID."
        ),
    )
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handles DELETE requests to remove a favorite property entry.
        """
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance: UserFavoriteProperty) -> None:
        """
        Performs the deletion of a UserFavoriteProperty instance.

        Ensures only the owner can delete their favorite.
        """
        user: CustomUserType = cast(CustomUserType, self.request.user)
        if instance.user != user:
            logger.warning(
                f"User {user.username} attempted to delete "
                f"favorite {instance.id} owned by {instance.user.username}."
            )
            # DRF's default permission_classes usually handle this,
            # but an explicit check within perform_destroy is also valid.
            # If you rely solely on permissions, you might remove this.
            raise PermissionDenied(
                detail=_("You do not have permission to delete this favorite.")
            )
        instance.delete()
        logger.info(
            f"User {user.username} successfully removed favorite "
            f"{instance.id} (property {instance.property.id})."
        )
