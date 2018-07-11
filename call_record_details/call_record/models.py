from django.db import models

class Record_model(models.Model):
    STARTED = 0
    ENDED = 1

    type_call = [
        (STARTED, 'Call started'),
        (ENDED, 'Call ended')
    ]

    type = models.IntegerField(choices=type_call, default=STARTED, verbose_name='Type of the call recored')
    timestamp = models.DateTimeField(verbose_name='Time of the call record')
    call_id = models.IntegerField(verbose_name='Call identifier')
    source = models.CharField(max_length=11, verbose_name='Origin phone number', blank=True)
    destination = models.CharField(max_length=11, verbose_name='Destination phone number', blank=True)