from django.contrib import admin

from .models import Record_model

class Record_admin(admin.ModelAdmin):
    list_display = ['call_id', 'origin_phone_number','type','time']

admin.site.register(Record_model, Record_admin)