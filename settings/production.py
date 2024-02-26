import environ

from .base import *

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
DEBUG = env('DEBUG')

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
