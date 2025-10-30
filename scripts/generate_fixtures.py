#!/usr/bin/env python3
"""
Generate a Django fixtures.json file for the `rides` app.
Creates Users, Rides, and RideEvents. Adjust counts below if you want more or fewer items.
"""

import json
import random
from datetime import datetime, timedelta, timezone

OUT_PATH = '/home/wayat/dev/ridez/fixtures.json'

random.seed(0)

# Configuration: hundreds of items
USERS_TOTAL = 150  # 100 riders, 40 drivers, 10 admins
RIDERS_COUNT = 100
DRIVERS_COUNT = 40
ADMINS_COUNT = USERS_TOTAL - RIDERS_COUNT - DRIVERS_COUNT

RIDES_COUNT = 400  # number of rides (create one event per ride)

PASSWORD_HASH = 'pbkdf2_sha256$260000$fixedsalt$fixedhashedpassword'
# Make the base date close to the current time so API testing sees recent timestamps
BASE_DATE = datetime.utcnow().replace(tzinfo=timezone.utc) - timedelta(days=3)

objects = []

# Users: pk 1..USERS_TOTAL
for i in range(1, USERS_TOTAL + 1):
    if i <= RIDERS_COUNT:
        role = 'rider'
        is_staff = False
        is_superuser = False
    elif i <= RIDERS_COUNT + DRIVERS_COUNT:
        role = 'driver'
        is_staff = False
        is_superuser = False
    else:
        role = 'admin'
        is_staff = True
        is_superuser = True

    obj = {
        'model': 'rides.user',
        'pk': i,
        'fields': {
            'password': PASSWORD_HASH,
            'last_login': None,
            'is_superuser': is_superuser,
            'username': f'user{i}',
            'first_name': f'User{i}',
            'last_name': 'Test',
            'email': f'user{i}@example.com',
            'is_staff': is_staff,
            'is_active': True,
            'date_joined': '2023-01-01T00:00:00Z',
            'role': role,
            'phone_number': f'+1555000{str(i).zfill(5)}',
        },
    }
    objects.append(obj)

# Rides: pk 1..RIDES_COUNT
statuses = ['en-route', 'pickup', 'dropoff']
# store pickup datetimes so RideEvent can reuse and build around them
pickup_times = {}

for r in range(1, RIDES_COUNT + 1):
    status = statuses[r % len(statuses)]
    # pick rider and driver PKs
    rider_pk = (r % RIDERS_COUNT) + 1
    # 10% of rides have no driver yet
    if random.random() < 0.1:
        driver_pk = None
    else:
        driver_pk = RIDERS_COUNT + (r % DRIVERS_COUNT) + 1  # drivers are after riders

    # deterministic coordinates around a city center (e.g., San Francisco-like)
    lat_offset = (r % 100) * 0.0007
    lon_offset = (r % 100) * 0.0009
    pickup_lat = 37.7000 + lat_offset
    pickup_lon = -122.4000 + lon_offset
    dropoff_lat = 37.8000 + ((r * 3) % 100) * 0.0006
    dropoff_lon = -122.5000 + ((r * 5) % 100) * 0.0008

    # randomize pickup_time within a realistic window so ordering isn't by ID
    # choose an offset between -7 days and +30 days (in minutes)
    offset_minutes = random.randint(-7 * 24 * 60, 30 * 24 * 60)
    # add a small r-dependent jitter so values aren't repeated too often
    jitter = r % 60
    # use timezone-aware datetimes relative to BASE_DATE
    pickup_time = BASE_DATE + timedelta(minutes=offset_minutes + jitter)
    pickup_times[r] = pickup_time
    pickup_time_iso = pickup_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    ride_obj = {
        'model': 'rides.ride',
        'pk': r,
        'fields': {
            'status': status,
            'id_rider': rider_pk,
            'id_driver': driver_pk,
            'pickup_latitude': round(pickup_lat, 6),
            'pickup_longitude': round(pickup_lon, 6),
            'dropoff_latitude': round(dropoff_lat, 6),
            'dropoff_longitude': round(dropoff_lon, 6),
            'pickup_time': pickup_time_iso,
        },
    }
    objects.append(ride_obj)

# RideEvents: now a ForeignKey relationship — generate multiple events per ride
event_pk = 1
# pick a few rides to be "chatty" and have many events
heavy_rides = set(random.sample(range(1, RIDES_COUNT + 1), k=min(6, RIDES_COUNT)))
for r in range(1, RIDES_COUNT + 1):
    pickup_dt = pickup_times.get(r, BASE_DATE + timedelta(minutes=r))

    # default number of events per ride: 1..4, but heavy_rides get many (10..25)
    if r in heavy_rides:
        events_count = random.randint(10, 25)
    else:
        events_count = random.randint(1, 4)

    for e_index in range(events_count):
        # spread events around pickup_time: from -120 minutes to +720 minutes
        offset = random.randint(-120, 720) + (e_index * 2)
        created_at_dt = pickup_dt + timedelta(minutes=offset)
        created_at = created_at_dt.strftime('%Y-%m-%dT%H:%M:%SZ')

        event_obj = {
            'model': 'rides.rideevent',
            'pk': event_pk,
            'fields': {
                'id_ride': r,
                'description': f'Event {e_index + 1} for ride {r}',
                'created_at': created_at,
            },
        }
        objects.append(event_obj)
        event_pk += 1

# Write to file
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(objects, f, indent=2)

print(f'Wrote {len(objects)} fixture objects to {OUT_PATH}')
