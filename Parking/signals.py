"""
Signals.py
"""

from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
from django.dispatch import receiver
# from .models import ParkingPlace, ParkingSpace


# @receiver(sender=ParkingPlace, signal=post_save)
# def create_parking_space(sender, instance, created, **kwargs):
#     """
#     Bulk Creating
#     """
#     print("create_parking_space")
#     if created:
#         print("create_parking_space 'created'")
#         parking_space = [
#             ParkingSpace(
#                 title=f"P{i}",
#                 parking_place=instance,
#             )
#             for i in range(instance.number_of_parkingspaces)
#         ]
#         ParkingSpace.objects.bulk_create(parking_space)
