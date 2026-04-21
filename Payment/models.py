from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.conf import settings
from Reservation.models import Reservation

User = settings.AUTH_USER_MODEL
# Create your models here.
@transaction.atomic
class Payment(models.Model):
    INITIATED = 'INITIATED'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reservation_id = models.OneToOneField(Reservation,on_delete=models.PROTECT)
    PAYMENT_STATUS = [(INITIATED , 'Initiated'),(SUCCESS , 'Success' ),(FAILED , 'Failed')]
    status = models.CharField(choices=(PAYMENT_STATUS),default='Initiated',max_length=9)
    amount = models.DecimalField(max_digits=8,decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} | {self.reservation_id} | {self.status} | {self.amount}'

    def save(self,*args,**kwargs):
        self.amount = self.reservation_id.total_price
        super().save(*args,**kwargs)

    def clean(self):
        if self.user.id != self.reservation_id:
            raise ValidationError("message : Payment Owner And Reservation Owner Must Be Same")
