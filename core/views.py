from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema


def home(request):
    return HttpResponse("Welcome to the Hardware Rental API!")

@swagger_auto_schema(method='get', tags=['Health'])
@api_view(['GET'])
def health_check(request):
    return Response({
        'status': 'healthy',
        'message': 'Eagle Horizon API is running'
    }, status=status.HTTP_200_OK)