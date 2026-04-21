from django.apps import AppConfig


class ParkingConfig(AppConfig):
    name = 'Parking'
    def ready(self):
        import Parking.signals
