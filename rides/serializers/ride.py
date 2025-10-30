from rest_framework import serializers
from rides.models import RideEvent, Ride
from rides.serializers.user import UserSerializer


class RideEventSerializer(serializers.ModelSerializer):
    id_ride_event = serializers.IntegerField(help_text='Unique identifier for the ride event.', read_only=True)
    description = serializers.CharField(help_text='Description of the ride event.')
    created_at = serializers.DateTimeField(help_text='Timestamp of when the event occurred.', read_only=True)

    class Meta:
        model = RideEvent
        exclude = ['id_ride']


class RideSerializer(serializers.ModelSerializer):
    id_ride = serializers.IntegerField(help_text='Unique identifier for the ride.', read_only=True)
    status = serializers.CharField(help_text='Current status of the ride.')
    driver = UserSerializer(source='id_driver', help_text='Driver details assigned to the ride.')
    rider = UserSerializer(source='id_rider', help_text='Rider details who requested the ride.')
    pickup_latitude = serializers.FloatField(help_text='Latitude of the pickup location.')
    pickup_longitude = serializers.FloatField(help_text='Longitude of the pickup location.')
    dropoff_latitude = serializers.FloatField(help_text='Latitude of the dropoff location.')
    dropoff_longitude = serializers.FloatField(help_text='Longitude of the dropoff location.')
    pickup_time = serializers.DateTimeField(help_text='Scheduled pickup time.')
    ride_events = RideEventSerializer(source='events', help_text='Event associated with the ride.')

    class Meta:
        model = Ride
        exclude = ['id_driver', 'id_rider']
