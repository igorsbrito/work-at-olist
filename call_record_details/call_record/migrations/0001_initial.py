# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record_model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('type', models.IntegerField(verbose_name='Type of the call recored', default=0, choices=[(0, 'Call started'), (1, 'Call ended')])),
                ('time', models.DateTimeField(verbose_name='Time of the call record')),
                ('call_id', models.IntegerField(verbose_name='Call identifier')),
                ('origin_phone_number', models.CharField(verbose_name='Origin phone number', max_length=11, blank=True)),
                ('destination_phone_number', models.CharField(verbose_name='Destination phone number', max_length=11, blank=True)),
            ],
        ),
    ]
