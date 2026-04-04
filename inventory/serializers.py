from django.conf import settings
from rest_framework import serializers
from .models import Hardware, EquipmentCategory, Equipment


class HardwareSerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField()

    def get_currency(self, obj):
        return settings.CURRENCY

    class Meta:
        model = Hardware
        fields = ['id', 'name', 'description', 'price_per_day', 'currency', 'total_quantity']


class EquipmentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentCategory
        fields = '__all__'
        read_only_fields = ('id',)
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': False, 'allow_blank': True, 'default': ''},
        }


class EquipmentCategoryNestedSerializer(serializers.ModelSerializer):
    """Read-only nested representation used inside EquipmentSerializer responses."""
    class Meta:
        model = EquipmentCategory
        fields = ('id', 'name')


class EquipmentSerializer(serializers.ModelSerializer):
    # Read: returns full category object. Write: accepts category ID.
    category_detail = EquipmentCategoryNestedSerializer(source='category', read_only=True)
    currency = serializers.SerializerMethodField()

    def get_currency(self, obj):
        return settings.CURRENCY

    class Meta:
        model = Equipment
        fields = [
            'id',
            'name',
            'category',        # write (FK id)
            'category_detail', # read (nested)
            'is_electric',
            'description',
            'total_quantity',
            'available_quantity',
            'condition',
            'price_per_day',
            'currency',
            'power_rating_watts',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ('id', 'category_detail', 'currency', 'available_quantity', 'created_at', 'updated_at')
        extra_kwargs = {
            'name': {
                'required': True,
            },
            'category': {
                'required': True,
                'write_only': True,
            },
            'price_per_day': {
                'required': True,
            },
            'total_quantity': {
                'required': True,
                'min_value': 1,
            },
            'is_electric': {
                'required': False,
                'default': False,
            },
            'description': {
                'required': False,
                'allow_blank': True,
                'default': '',
            },
            'condition': {
                'required': False,
            },
            'power_rating_watts': {
                'required': False,
                'allow_null': True,
                'min_value': 1,
            },
        }

    def validate(self, attrs):
        is_electric = attrs.get('is_electric', False)
        power_rating = attrs.get('power_rating_watts')
        if is_electric and not power_rating:
            raise serializers.ValidationError({
                'power_rating_watts': 'Power rating (watts) is required for electric equipment.'
            })
        return attrs

    def create(self, validated_data):
        # available_quantity starts equal to total_quantity on creation
        validated_data['available_quantity'] = validated_data['total_quantity']
        return super().create(validated_data)