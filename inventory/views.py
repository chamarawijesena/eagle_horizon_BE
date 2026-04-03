from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Hardware, EquipmentCategory, Equipment
from .serializers import HardwareSerializer, EquipmentCategorySerializer, EquipmentSerializer


class HardwareViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hardware.objects.all()
    serializer_class = HardwareSerializer


class EquipmentCategoryViewSet(viewsets.ModelViewSet):
    queryset = EquipmentCategory.objects.all()
    serializer_class = EquipmentCategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.select_related('category').all()
    serializer_class = EquipmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_electric', 'condition']
    search_fields = ['name', 'description', 'category__name']
