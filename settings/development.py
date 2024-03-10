import os

from .base import *

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST_POSTGRES"),
        "PORT": os.environ.get("DATABASE_PORT_POSTGRES"),
    }
}

###############################
# CUSTOM DEVELOPMENT SETTINGS #
###############################

CSRF_COOKIE_SECURE = False

allowed_origin_env = os.getenv("CORS_ALLOWED_ORIGINS")
if allowed_origin_env:
    CORS_ALLOWED_ORIGINS = allowed_origin_env.split(",")

if os.getenv("CORS_ALLOW_CREDENTIALS") == "true":
    CORS_ALLOW_CREDENTIALS = True
