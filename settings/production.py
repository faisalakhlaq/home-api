# NOTE we are using `django-environ` specifically for pythonganywhere because os.environ.get() won't work
# If the deployment from pythonanywhere is changed then we can remove the django-environ package from
# production requirements.
import os

import environ  # specifically for pythonganywhere

from .base import *

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    # explicity set that it to signal its not CI environment.
    # If its CI env then it will be overwritten
    DJANGO_CI_ENV=(bool, False),
)

# Check if DJANGO_CI_ENV is False (i.e., not in CI)
if not env.bool("DJANGO_CI_ENV"):
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

CORS_ALLOW_ALL_ORIGINS = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

###########
# LOGGING #
###########

LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING: LoggingConfig = BASE_LOGGING.copy()

LOGGING["handlers"]["file"]["filename"] = os.path.join(BASE_DIR, "logs", "django.log")

for _, logger_config in LOGGING["loggers"].items():
    if "handlers" in logger_config:
        logger_config["handlers"] = ["file"]

# Specific logging for production
LOGGING["loggers"]["django.request"] = {
    "handlers": ["file"],
    "level": "ERROR",
    "propagate": False,
}

# Allauth settings (CRITICAL FOR EMAIL-BASED AUTH)
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# ACCOUNT_EMAIL_VERIFICATION = "optional" # Let the users log in immediately

# Email Backend settings (ESSENTIAL for email verification)
# Configure a real email service (e.g., SendGrid, Mailgun, AWS SES)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.yourdomain.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@yourdomain.com'
# EMAIL_HOST_PASSWORD = 'your-email-password'
# DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com' # Or a specific sender email
