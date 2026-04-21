from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from Parking.models import Organization, Location, ParkingSpot, VehicleTypeSpported
from .serializers import ReservationSerializer


class ReservationTimeValidationTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create_user(
            email='owner@example.com',
            password='secret',
            first_name='Owner',
            last_name='One',
            roll='PO',
        )
        self.driver = User.objects.create_user(
            email='driver@example.com',
            password='secret',
            first_name='Driver',
            last_name='Two',
            roll='D',
        )

        self.organization = Organization.objects.create(
            owner=self.owner,
            name='Test Parking',
            city='Test City',
        )
        self.location = Location.objects.create(
            owner=self.owner,
            country='Test Country',
            city='Test City',
            area='Test Area',
        )
        self.vehicle_supported = VehicleTypeSpported.objects.create(
            owner=self.owner,
            vehicle_type='L',
            price_per_hour=15.00,
        )
        self.parking_spot = ParkingSpot.objects.create(
            title='Spot A',
            description='Test spot',
            organization=self.organization,
            location=self.location,
            status='A',
        )
        self.parking_spot.vehicle_supported.add(self.vehicle_supported)
        self.request = type('Request', (), {'user': self.driver})()

    def _make_data(self, start_time, end_time):
        return {
            'parking_spot': self.parking_spot.pk,
            'vehicle_type': 'L',
            'start_time': start_time,
            'end_time': end_time,
        }

    def test_start_time_cannot_be_in_the_past(self):
        start_time = timezone.now() - timedelta(minutes=10)
        end_time = timezone.now() + timedelta(hours=1)

        serializer = ReservationSerializer(
            data=self._make_data(start_time, end_time),
            context={'request': self.request},
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('start_time', serializer.errors)
        self.assertEqual(serializer.errors['start_time'][0], 'Start time cannot be in the past.')

    def test_start_time_must_be_at_least_five_minutes_from_now(self):
        start_time = timezone.now() + timedelta(minutes=3)
        end_time = timezone.now() + timedelta(hours=1)

        serializer = ReservationSerializer(
            data=self._make_data(start_time, end_time),
            context={'request': self.request},
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('start_time', serializer.errors)
        self.assertEqual(serializer.errors['start_time'][0], 'Start time must be at least 5 minutes from now.')

    def test_end_time_must_be_after_start_time(self):
        start_time = timezone.now() + timedelta(minutes=10)
        end_time = start_time

        serializer = ReservationSerializer(
            data=self._make_data(start_time, end_time),
            context={'request': self.request},
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('end_time', serializer.errors)
        self.assertEqual(serializer.errors['end_time'][0], 'End time must be after start time.')

    def test_valid_reservation_time_is_allowed(self):
        start_time = timezone.now() + timedelta(minutes=10)
        end_time = timezone.now() + timedelta(hours=1)

        serializer = ReservationSerializer(
            data=self._make_data(start_time, end_time),
            context={'request': self.request},
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        reservation = serializer.save()
        self.assertEqual(reservation.driver, self.driver)
        self.assertGreater(reservation.total_price, 0)
