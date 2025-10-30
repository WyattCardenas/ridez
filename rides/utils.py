from datetime import datetime, timedelta
from functools import partial

from django.utils import timezone


def get_time_before(*_, **kwargs) -> datetime:
    return timezone.now() - timedelta(**kwargs)


twenty_four_hours_ago = partial(get_time_before, hours=24)
