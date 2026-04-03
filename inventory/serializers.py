from rest_framework import serializers
from .models import Hardware, EquipmentCategory, Equipment


class HardwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hardware
        fields = "__all__"


class EquipmentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentCategory
        fields = '__all__'
        read_only_fields = ('id',)


class EquipmentSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Equipment
        fields = [
            'id',
            'name',
            'category',
            'category_name',
            'is_electric',
            'description',
            'total_quantity',
            'available_quantity',
            'condition',
            'price_per_day',
            'power_rating_watts',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')
