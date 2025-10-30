from rest_framework.routers import DefaultRouter
from rides.api.ride import RideViewSet

router = DefaultRouter()
router.register(r'rides', RideViewSet)

urlpatterns = []
urlpatterns += router.urls
