from django.contrib import admin
from .models import Hardware, EquipmentCategory, Equipment


@admin.register(Hardware)
class HardwareAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_day', 'total_quantity')
    search_fields = ('name',)


@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'is_electric',
        'condition',
        'total_quantity',
        'available_quantity',
        'price_per_day',
    )
    list_filter = ('is_electric', 'condition', 'category')
    search_fields = ('name', 'description', 'category__name')
