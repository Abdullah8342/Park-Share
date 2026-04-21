from django.contrib import admin
from .models import (
    Location,
    VehicleTypeSpported,
    Organization,
    ParkingSpot
)
# Register your models here.

admin.site.register(Location)
admin.site.register(VehicleTypeSpported)
admin.site.register(Organization)
admin.site.register(ParkingSpot)

