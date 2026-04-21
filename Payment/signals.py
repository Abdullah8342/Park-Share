from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Payment
from Reservation.models import Reservation

@receiver(post_save,sender=Payment)
def update_status(sender,instance,created,**kwargs):
    print("DEBUG : update_status")
    if created:
        print("DEBUG : update_status if created")
        reservation_object = get_object_or_404(Reservation,id = instance.reservation_id)
        reservation_object.status = "CONFIRMED"
        reservation_object.save()

