'''
    Parking
'''
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VehicleTypeSpportedViewset,
    LocationViewset,
    OrganizationViewset,
    ParkingSpotViewset
)

router = DefaultRouter()
router.register("location",LocationViewset,basename='location')
router.register("type-supported", VehicleTypeSpportedViewset, basename="type-supported")
router.register("organization", OrganizationViewset)
router.register("spot", ParkingSpotViewset)


urlpatterns = [
    path("api/", include(router.urls)),
]
