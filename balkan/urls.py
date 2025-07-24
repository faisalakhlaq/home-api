from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("api/v1/control-center/", admin.site.urls),
    path("api/v1/", include("apps.properties.urls")),
    path("api/v1/", include("apps.users.urls")),
    path("api/v1/", include("apps.favorites.urls")),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI endpoint
    path(
        "api/v1/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # ReDoc UI endpoint
    path(
        "api/v1/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
