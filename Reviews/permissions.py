from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from Parking.models import ParkingSpot
from Reservation.models import Reservation


class ReservationUserCanReview(permissions.BasePermission):
    message = 'Only users who reserved this parking space may leave a review.'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.method == 'POST':
            parking_space_id = request.data.get('parking_space')
            if not parking_space_id:
                return False

            try:
                parking_space = ParkingSpace.objects.get(pk=parking_space_id)
            except (ParkingSpace.DoesNotExist, ValueError, TypeError):
                return False

            return Reservation.objects.filter(
                parking_space=parking_space,
                driver=request.user,
            ).exists()

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.reviewer == request.user
