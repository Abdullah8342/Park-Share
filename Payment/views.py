from rest_framework import viewsets
from .serializers import PaymentSerializers
from .models import Payment
# Create your views here.

class PaymentViewset(viewsets.ModelViewSet):
    serializer_class = PaymentSerializers
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
