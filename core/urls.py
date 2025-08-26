from rest_framework import routers
from .views import TestViewSet

router = routers.DefaultRouter()
router.register(r'TestModel', TestViewSet)

urlpatterns = router.urls