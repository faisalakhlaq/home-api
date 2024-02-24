import os

from django.core.wsgi import get_wsgi_application

if os.environ.get("DEBUG"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production")

application = get_wsgi_application()
