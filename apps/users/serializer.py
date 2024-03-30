from rest_framework.serializers import ModelSerializer

# from dj_rest_auth.registration.serializers import RegisterSerializer

from .models import User


class AuthUserDetailsSerializer(ModelSerializer[User]):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "is_business_user",
            "is_company_admin",
        )
        read_only_fields = (
            "email",
            "username",
        )


# class CusomRegisterSerializer(RegisterSerializer):
#     first_name = CharField()
#     last_name = CharField()
#     email = EmailField()
