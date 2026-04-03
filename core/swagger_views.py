from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class EagleTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Extends the default JWT serializer to embed role in the token and response."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = cls._resolve_role(user)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': self._resolve_role(user),
        }
        return data

    @staticmethod
    def _resolve_role(user):
        if user.is_superuser:
            return 'SUPER_ADMIN'
        try:
            return user.profile.role
        except Exception:
            return 'VIEWER'


# Swagger response schema
class TokenResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = serializers.DictField()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = EagleTokenObtainPairSerializer

    @swagger_auto_schema(
        tags=['Auth'],
        responses={200: TokenResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RefreshTokenView(TokenRefreshView):
    @swagger_auto_schema(
        tags=['Auth'],
        responses={200: TokenResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)