from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer
from .permissions import ReservationUserCanReview


class ReviewViewset(viewsets.ModelViewSet):
    '''
        Review Viewset
    '''
    permission_classes = [permissions.IsAuthenticated, ReservationUserCanReview]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
