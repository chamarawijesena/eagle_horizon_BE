from rest_framework import viewsets
from .models import Hardware
from .serializers import HardwareSerializer

class HardwareViewSet(viewsets.ModelViewSet):
    queryset = Hardware.objects.all()
    serializer_class = HardwareSerializer
