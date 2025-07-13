# NOTE we are using `django-environ` specifically for pythonganywhere because os.environ.get() won't work
# If the deployment from pythonanywhere is changed then we can remove the django-environ package from
# production requirements.
import os

import environ  # specifically for pythonganywhere

from .base import *

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    # explicity set that it to signal its not CI environment. If it CI env then it will be overwritten
    DJANGO_CI_ENV=(bool, False),
)

if not env.bool("DJANGO_CI_ENV"):  # Check if DJANGO_CI_ENV is False (i.e., not in CI)
    environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")
if ALLOWED_HOSTS:
    ALLOWED_HOSTS = ALLOWED_HOSTS.split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DATABASE_NAME_MYSQL"),
        "USER": env("DATABASE_USER_MYSQL"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST_MYSQL"),
        "PORT": env("DATABASE_PORT_MYSQL"),
    }
}

CORS_ORIGIN_ALLOW_ALL = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
