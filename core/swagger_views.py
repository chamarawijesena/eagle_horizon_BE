from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import serializers

# 1. Define a serializer for the RESPONSE so Swagger can show it
class TokenResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

class MyTokenObtainPairView(TokenObtainPairView):
    # Use the default SimpleJWT serializer for logic, but keep your custom one for Swagger UI
    @swagger_auto_schema(
        responses={200: TokenResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class RefreshTokenView(TokenRefreshView):
    @swagger_auto_schema(
        responses={200: TokenResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
