from django.contrib import admin
from rides.models import User, RideEvent

admin.site.register(User)


@admin.register(RideEvent)
class RideEventAdmin(admin.ModelAdmin):
    list_display = ('id_ride_event', 'id_ride', 'description', 'created_at')
    readonly_fields = ('created_at',)
