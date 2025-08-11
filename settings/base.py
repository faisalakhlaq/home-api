import os
from datetime import timedelta
from pathlib import Path
from typing import List

from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", default=get_random_secret_key())

# Application definition
THIRD_PARTY_APPS: List[str] = [
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",  # for social authentication
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "django_filters",
    "corsheaders",
    "drf_spectacular",
]
BASE_PROJECT_APPS: List[str] = [
    "apps.users",
    "apps.core",
    "apps.locations",
    "apps.properties",
    "apps.favorites",
]
INSTALLED_APPS = (
    [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]
    + BASE_PROJECT_APPS
    + THIRD_PARTY_APPS
)

SITE_ID = 1

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ROOT_URLCONF = "balkan.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "static")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "balkan.wsgi.application"
AUTH_USER_MODEL = "users.User"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    # 3.0 gives you the option to serialize decimals as floats.
    # if COERCE_DECIMAL_TO_STRING then the decimals are serialized as strings.
    "COERCE_DECIMAL_TO_STRING": False,
    "NON_FIELD_ERRORS_KEY": "detail",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": False,
    "REGISTER_SERIALIZER": "apps.users.serializers.CustomRegisterSerializer",
    "LOGIN_SERIALIZER": "apps.users.serializers.CustomLoginSerializer",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "SIGNING_KEY": "complexsigningkey",  # generate a key and replace me
    "ALGORITHM": "HS512",
}

# django-allauth settings for signup fields
ACCOUNT_SIGNUP_FIELDS = {
    "email": {"required": True, "label": "Email Address*", "widget": "email"},
    "first_name": {
        "required": True,
        "label": "First Name*",
    },
    "last_name": {
        "required": True,
        "label": "Last Name*",
    },
}

# Allauth settings (CRITICAL FOR EMAIL-BASED AUTH)
# If custom User model *doesn't* have a `username` field, therefore:
ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # We removed username from CustomUser
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGIN_METHODS = ["email"]  # Users log in using their email address

# Email Backend settings (ESSENTIAL for email verification)
# For development, use console backend to see emails in your terminal
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SPECTACULAR_SETTINGS = {
    "TITLE": "Balkan Real Estate API Documentation",
    "DESCRIPTION": "API for Balkan home project.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
