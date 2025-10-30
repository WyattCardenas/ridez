import logging
from enum import StrEnum
from typing import TYPE_CHECKING

from django.db.models import ExpressionWrapper, F, FloatField, Prefetch
from django.db.models.functions import ATan2, Cos, Radians, Sin, Sqrt
from django.http import Http404
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet

from rides.api.permissions import IsAdmin
from rides.models import Ride, RideEvent, RideStatus
from rides.serializers.ride import RideSerializer
from rides.utils import twenty_four_hours_ago

if TYPE_CHECKING:
    from django_filters.rest_framework import FilterSet
    from rest_framework.filters import BaseFilterBackend

logger = logging.getLogger('rides.api.ride')


class RideFilter(filters.FilterSet):
    status = filters.MultipleChoiceFilter(label='Ride status', field_name='status', choices=RideStatus.choices)
    rider_email = filters.CharFilter(
        label="Rider's email address", field_name='id_rider__email', lookup_expr='icontains'
    )
    lat = filters.NumberFilter(
        label='Latitude',
        help_text='Latitude. Used in conjunction with "lon" for distance ordering. Will <b>not</b> filter results.',
        method='set_latitude',
    )
    lon = filters.NumberFilter(
        label='Longitude',
        help_text='Longitude. Used in conjunction with "lat" for distance ordering. Will <b>not</b> filter results.',
        method='set_longitude',
    )

    def set_latitude(self, queryset, name, value):
        # Do nothing, only used to display field in DRF browsable API
        return queryset

    def set_longitude(self, queryset, name, value):
        # Do nothing, only used to display field in DRF browsable API
        return queryset

    class Meta:
        model = Ride
        fields = ['status', 'rider_email']


class DistanceOrderingFilter(OrderingFilter):
    KEY = 'distance'
    LAT_PARAM = 'lat'
    LON_PARAM = 'lon'

    class Origin(StrEnum):
        PICKUP_LATITUDE = 'pickup_latitude'
        PICKUP_LONGITUDE = 'pickup_longitude'
        DROPOFF_LATITUDE = 'dropoff_latitude'
        DROPOFF_LONGITUDE = 'dropoff_longitude'

    def filter_queryset(self, request, queryset, view):
        ordering: list[str] = self.get_ordering(request, queryset, view)

        if not ordering:
            return queryset

        if self.KEY not in [field.lstrip('-') for field in ordering]:
            return queryset.order_by(*ordering)

        try:
            user_lat = float(request.query_params.get(self.LAT_PARAM))
            user_lon = float(request.query_params.get(self.LON_PARAM))
        except (TypeError, ValueError):
            error = f'Latitude (key: {self.LAT_PARAM}) and longitude (key: {self.LAT_PARAM}) must be provided as valid numbers when ordering by distance.'
            logger.exception(error)
            raise Http404(error)

        # Haversine forula (https://en.wikipedia.org/wiki/Haversine_formula)
        # Patterned from: https://www.movable-type.co.uk/scripts/latlong.html
        # 1. Convert degrees to radians
        # 2. Calculate differences in lat and lon between points
        # 3. Apply Haversine formula (atan^2 version for numerical stability according to internet)
        # 4. Multiply by Earth's radius (in kilometers)
        # Full Formula: radius * 2 * atan2( sqrt(Sin(lat/2)^2 + Cos(lat1)*Cos(lat2)*Sin(lon/2)^2), sqrt(1 - (Sin(lat/2)^2 + Cos(lat1)*Cos(lat2)*Sin(lon/2)^2)) )
        def haversine_formula_expr(
            *,
            origin_lat: self.Origin = self.Origin.PICKUP_LATITUDE,
            origin_lon: self.Origin = self.Origin.PICKUP_LONGITUDE,
        ) -> ExpressionWrapper:
            EARTH_RADIUS_KM: float = 6371.0

            lat_delta = Radians(F(origin_lat)) - Radians(user_lat)
            lon_delta = Radians(F(origin_lon)) - Radians(user_lon)
            a = (
                Sin((lat_delta) / 2) ** 2
                + Cos(Radians(user_lat)) * Cos(Radians(F(origin_lat))) * Sin(lon_delta / 2) ** 2
            )

            return ExpressionWrapper(
                expression=(EARTH_RADIUS_KM * 2 * ATan2(Sqrt(a), Sqrt(1 - a))),
                output_field=FloatField(),
            )

        queryset = queryset.annotate(distance=haversine_formula_expr())
        return queryset.order_by(*ordering)


def get_filter_backends() -> list['FilterSet | BaseFilterBackend']:
    filter_backends_without_ordering = [
        backend for backend in api_settings.DEFAULT_FILTER_BACKENDS if backend != OrderingFilter
    ]
    filter_backends_for_this_api = [DistanceOrderingFilter]

    logger.info(
        'Overriding filterbackends for rides API, filtered defaults: %s, this API: %s',
        filter_backends_without_ordering,
        filter_backends_for_this_api,
    )
    return filter_backends_without_ordering + filter_backends_for_this_api


class RideViewSet(ModelViewSet):
    queryset = (
        Ride.objects.select_related('id_rider', 'id_driver')
        .prefetch_related(Prefetch('events', RideEvent.objects.filter(created_at__gt=twenty_four_hours_ago())))
        .all()
    )
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filterset_class = RideFilter
    ordering_fields = ['pickup_time', 'distance']
    filter_backends = get_filter_backends()
