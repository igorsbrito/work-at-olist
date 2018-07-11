from django.contrib import admin

from .models import Telephone_bill_call_model

class Telephone_bill_call_admin(admin.ModelAdmin):
    list_display = ['call_id', 'source','call_duration','call_price']

admin.site.register(Telephone_bill_call_model, Telephone_bill_call_admin)