from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from rides.api.permissions import IsAdmin
from rides.models import Ride
from rides.serializers.ride import RideSerializer


class RideViewSet(ModelViewSet):
    queryset = Ride.objects.select_related('id_rider', 'id_driver').prefetch_related('events').all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
