from rest_framework.routers import DefaultRouter
from .views import HardwareViewSet, EquipmentCategoryViewSet, EquipmentViewSet

router = DefaultRouter()
router.register(r'hardware', HardwareViewSet)
router.register(r'equipment-categories', EquipmentCategoryViewSet)
router.register(r'equipment', EquipmentViewSet)

urlpatterns = router.urls
