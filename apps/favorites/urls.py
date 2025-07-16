from rest_framework.routers import DefaultRouter

from apps.favorites.views import UserFavoritePropertyViewSet

app_name = "apps.favorites"
router = DefaultRouter()
router.register(r"favorites", UserFavoritePropertyViewSet, basename="favorite")
urlpatterns = router.urls
