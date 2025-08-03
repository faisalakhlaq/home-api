from typing import Any

from .app_settings import (
    JWTSerializer as JWTSerializer,
    JWTSerializerWithExpiration as JWTSerializerWithExpiration,
    LoginSerializer as LoginSerializer,
    PasswordChangeSerializer as PasswordChangeSerializer,
    PasswordResetConfirmSerializer as PasswordResetConfirmSerializer,
    PasswordResetSerializer as PasswordResetSerializer,
    TokenSerializer as TokenSerializer,
    UserDetailsSerializer as UserDetailsSerializer,
    create_token as create_token,
)
from .models import get_token_model as get_token_model
from .utils import jwt_encode as jwt_encode

from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView

class LoginView(GenericAPIView):
    permission_classes: Any
    serializer_class: Any
    throttle_scope: str
    user: Any
    access_token: Any
    token: Any
    request: Any
    serializer: Any

class LogoutView(APIView):
    permission_classes: Any
    throttle_scope: str

class UserDetailsView(RetrieveUpdateAPIView):
    serializer_class: Any
    permission_classes: Any
