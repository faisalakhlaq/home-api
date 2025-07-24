from django.urls import path

from rest_framework.routers import DefaultRouter

from apps.properties.views import PropertySearchAPI, PropertyViewSet

app_name = "apps.properties"

router = DefaultRouter()

router.register("properties", PropertyViewSet, basename="properties")

urlpatterns = router.urls + [
    path("properties/search/", PropertySearchAPI.as_view(), name="property-search"),
]
