from django.apps import AppConfig


class PaymentConfig(AppConfig):
    name = 'Payment'
    def ready(self):
        import Payment.signals
