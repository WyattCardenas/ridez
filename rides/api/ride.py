from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from rides.api.permissions import IsAdmin
from rides.models import Ride, RideStatus
from rides.serializers.ride import RideSerializer
from django_filters import rest_framework as filters


class RideFilter(filters.FilterSet):
    status = filters.MultipleChoiceFilter(label='Ride status', field_name='status', choices=RideStatus.choices)
    rider_email = filters.CharFilter(
        label="Rider's email address", field_name='id_rider__email', lookup_expr='icontains'
    )


class RideViewSet(ModelViewSet):
    queryset = Ride.objects.select_related('id_rider', 'id_driver').prefetch_related('events').all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filterset_class = RideFilter
