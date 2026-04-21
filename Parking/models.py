'''
    Parking
'''

from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL

class Location(models.Model):
    '''
        Location
    '''
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='location')
    country = models.CharField(max_length=125)
    city = models.CharField(max_length=125)
    area = models.CharField(max_length=125)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.owner} | {self.country} | {self.city} | {self.area}"

    class Meta:
        unique_together = [["city","area"]]


class VehicleTypeSpported(models.Model):
    '''
        Vehicle Type Supported
    '''
    LTV = 'LTV'
    HTV = 'HTV'
    MCW = 'MCW'
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='vehicle_type_spported')
    VEHICLE_TYPE_CHOICES = [('L',LTV),('H',HTV),('M',MCW)]
    vehicle_type = models.CharField(max_length=3)
    price_per_hour = models.DecimalField(max_digits=8,decimal_places=2)

    def __str__(self):
        return f"{self.vehicle_type} | {self.price_per_hour}"



class Organization(models.Model):
    '''
        parking place
    '''
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='organization')
    name = models.CharField(max_length=225)
    city = models.CharField(max_length=220)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.title} | {self.number_of_parkingspaces}"




class ParkingSpot(models.Model):
    '''
        parking_spot
    '''
    AVAILABLE = 'AVAILABLE'
    UNAVAILABLE = 'UNAVAILABLE'
    ARCHIVED = 'ARCHIVED'
    title = models.CharField(max_length=125)
    description = models.TextField(blank=True)
    STATUS_CHOICES = [('A',AVAILABLE),('U',UNAVAILABLE),('AR',ARCHIVED)]
    organization = models.ForeignKey(
        Organization,on_delete=models.CASCADE,related_name='parking_spot'
    )
    location = models.OneToOneField(Location,on_delete=models.PROTECT,related_name='parking_spot')
    vehicle_supported = models.ManyToManyField(
        VehicleTypeSpported,related_name='parking_spot'
    )
    status = models.CharField(choices=STATUS_CHOICES,default='A')


    def __str__(self):
        return f"{self.parking_place} | {self.title} | {self.status}"
