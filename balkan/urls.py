from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/v1/control-center/", admin.site.urls),
    path("api/v1/properties/", include("apps.properties.urls")),
]
