from rest_framework.routers import DefaultRouter
from .views import HardwareViewSet

router = DefaultRouter()
router.register(r'hardware', HardwareViewSet)

urlpatterns = router.urls
