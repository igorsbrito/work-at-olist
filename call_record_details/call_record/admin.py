from django.contrib import admin

from .models import Record_model

class Record_admin(admin.ModelAdmin):
    list_display = ['call_id', 'source','type','timestamp']

admin.site.register(Record_model, Record_admin)