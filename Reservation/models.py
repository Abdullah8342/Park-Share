from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils import timezone

from Parking.models import ParkingSpot


class Reservation(models.Model):
    """
    Reservation
    """

    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (CONFIRMED, "Confirmed"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
    ]

    LTV = "LTV"
    HTV = "HTV"
    MCW = "MCW"

    VEHICLE_TYPE_CHOICES = [
        ("L", LTV),
        ("H", HTV),
        ("M", MCW),
    ]

    parking_spot = models.ForeignKey(
        ParkingSpot, on_delete=models.PROTECT, related_name="reservations"
    )

    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations"
    )
    vehicle_type = models.CharField(max_length=3, choices=VEHICLE_TYPE_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        now = timezone.now()
        min_start_time = now + timedelta(minutes=5)

        if self.start_time < now:
            raise ValidationError({"start_time": "Start time cannot be in the past."})

        if self.start_time < min_start_time:
            raise ValidationError({"start_time": "Start time must be at least 5 minutes from now."})

        if self.end_time <= self.start_time:
            raise ValidationError({"end_time": "End time must be after start time."})

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.total_price:
            duration_hours = (self.end_time - self.start_time).total_seconds() / 3600
            vehicle_supported = (
                self.parking_spot.vehicle_supported.filter(
                    vehicle_type=self.vehicle_type
                ).first()
            )
            if vehicle_supported:
                self.total_price = float(duration_hours) * float(
                    vehicle_supported.price_per_hour
                )
            else:
                raise self.DoesNotExist("Message : Vehicle Type Does Not Supported")
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Reservation #{self.pk} - {self.status}"
