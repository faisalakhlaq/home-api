from dj_rest_auth.views import UserDetailsView

from rest_framework.permissions import IsAuthenticated

from .serializers import AuthUserDetailsSerializer


class AuthUserDetailsView(UserDetailsView):
    serializer_class = AuthUserDetailsSerializer
    permission_classes = [IsAuthenticated]
