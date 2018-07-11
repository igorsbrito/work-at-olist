from django.db import models

class Telephone_bill_call_model(models.Model):

    call_id = models.IntegerField(verbose_name='Call identifier')
    source = models.CharField(max_length=11, verbose_name='Origin phone number')
    destination = models.CharField(max_length=11, verbose_name='Destination phone number')

    call_price = models.DecimalField(max_digits=9, decimal_places=2)

    call_start = models.DateTimeField(verbose_name="call start date")
    call_end = models.DateTimeField(verbose_name="call end date")
    call_duration = models.TimeField(verbose_name="duration of the call")
