from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Hardware, EquipmentCategory, Equipment
from .serializers import HardwareSerializer, EquipmentCategorySerializer, EquipmentSerializer


@method_decorator(name='list',     decorator=swagger_auto_schema(tags=['Inventory']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Inventory']))
class HardwareViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hardware.objects.all()
    serializer_class = HardwareSerializer


@method_decorator(name='list',           decorator=swagger_auto_schema(tags=['Inventory']))
@method_decorator(name='create',         decorator=swagger_auto_schema(tags=['Inventory']))
@method_decorator(name='retrieve',       decorator=swagger_auto_schema(tags=['Inventory']))
@method_decorator(name='update',         decorator=swagger_auto_schema(tags=['Inventory']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Inventory']))
@method_decorator(name='destroy',        decorator=swagger_auto_schema(tags=['Inventory']))
class EquipmentCategoryViewSet(viewsets.ModelViewSet):
    queryset = EquipmentCategory.objects.all()
    serializer_class = EquipmentCategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


@method_decorator(name='list',           decorator=swagger_auto_schema(tags=['Inventory']))
@method_decorator(name='create',         decorator=swagger_auto_schema(tags=['Inventory']))
@method_decorator(name='retrieve',       decorator=swagger_auto_schema(tags=['Inventory']))
@method_decorator(name='update',         decorator=swagger_auto_schema(tags=['Inventory']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Inventory']))
@method_decorator(name='destroy',        decorator=swagger_auto_schema(tags=['Inventory']))
class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.select_related('category').all()
    serializer_class = EquipmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_electric', 'condition']
    search_fields = ['name', 'description', 'category__name']
