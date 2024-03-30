from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/v1/control-center/", admin.site.urls),
    path("api/v1/properties/", include("apps.properties.urls")),
    path("api/v1/users/", include("apps.users.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore
