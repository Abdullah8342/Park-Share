from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from Parking.models import ParkingSpot


class Review(models.Model):
    '''
        Review
    '''
    parking_spot = models.ForeignKey(
        ParkingSpot,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Review #{self.pk} for {self.parking_space}'
