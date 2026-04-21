'''
    views.py
'''
from rest_framework import viewsets
from .permissions import IsOwner,IsOwnerOrReadOnly,IsSpotOwnerOrReadOnly

from .models import (
    Location,
    VehicleTypeSpported,
    Organization,
    ParkingSpot
)
from .serializers import (
    LocationSerializer,
    VehicleTypeSpportedSerializer,
    OrganizationSerializer,
    ParkingSpotSerializer
)

class LocationViewset(viewsets.ModelViewSet):
    '''
        Location
    '''
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Location.objects.filter(owner = self.request.user)
    serializer_class = LocationSerializer

    def get_serializer_context(self):
        context = {'request':self.request}
        return context



class VehicleTypeSpportedViewset(viewsets.ModelViewSet):
    '''
        VehicleTypeSpportedViewset
    '''
    permission_classes = [IsOwner]
    def get_queryset(self):
        return VehicleTypeSpported.objects.filter(owner = self.request.user)
    serializer_class = VehicleTypeSpportedSerializer

    def get_serializer_context(self):
        context = {"request": self.request}
        return context


class OrganizationViewset(viewsets.ModelViewSet):
    '''
        Parking Place Viewset
    '''
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_serializer_context(self):
        context = {"request": self.request}
        return context





class ParkingSpotViewset(viewsets.ModelViewSet):
    '''
        Parking Space Viewset
    '''
    permission_classes = [IsSpotOwnerOrReadOnly]
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotSerializer

    def get_serializer_context(self):
        context = {"request": self.request}
        return context
