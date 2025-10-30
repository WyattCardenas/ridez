from django.db import models
from django.contrib.auth.models import AbstractUser


PHONE_NUMBER_GLOBAL_MAX_LENGTH = 16  # E.164 standard maximum length + the '+' sign


class RideStatus(models.TextChoices):
    ENROUTE = 'en-route', 'En-route'
    PICKUP = 'pickup', 'Pickup'
    DROPOFF = 'dropoff', 'Dropoff'


class Roles(models.TextChoices):
    RIDER = 'rider', 'Rider'
    DRIVER = 'driver', 'Driver'
    ADMIN = 'admin', 'Admin'


class User(AbstractUser):
    id_user = models.BigAutoField(primary_key=True)
    role = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=PHONE_NUMBER_GLOBAL_MAX_LENGTH, unique=True)


class Ride(models.Model):
    id_ride = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=8, choices=RideStatus.choices, default=RideStatus.ENROUTE)
    id_rider = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='rider', null=True)
    id_driver = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='driver', null=True)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()


class RideEvent(models.Model):
    id_ride_event = models.BigAutoField(primary_key=True)
    id_ride = models.OneToOneField(Ride, on_delete=models.CASCADE, related_name='events')
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
