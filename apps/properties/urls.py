from rest_framework.routers import DefaultRouter

from apps.properties.views import PropertyViewSet

app_name = "apps.properties"

router = DefaultRouter()

router.register("properties", PropertyViewSet, basename="properties")

urlpatterns = router.urls
