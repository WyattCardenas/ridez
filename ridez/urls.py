from django.contrib import admin
from django.conf import settings
from django.urls import include, path

from rides.urlconf import urlpatterns as ride_urls

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns.extend(ride_urls)

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
