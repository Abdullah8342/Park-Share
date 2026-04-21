from rest_framework import viewsets,permissions
from .serializers import ReservationSerializer
from .models import Reservation
# Create your views here.
from .permissions import IsDriverOnly

class ReservationViewset(viewsets.ModelViewSet):
    '''
        Reservation Viewset
    '''
    permission_classes = [permissions.IsAuthenticated,IsDriverOnly]
    def get_queryset(self):
        return Reservation.objects.filter(driver = self.request.user)
    serializer_class = ReservationSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
