from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse


def home(request):
    return HttpResponse("Welcome to the Hardware Rental API!")

@api_view(['GET'])
def health_check(request):
    """Health check endpoint."""
    return Response({
        'status': 'healthy',
        'message': 'Eagle Horizon API is running'
    }, status=status.HTTP_200_OK)
