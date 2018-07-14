from rest_framework import serializers

from .models import Telephone_bill_call_model

class Telephone_bill_call_serializer(serializers.ModelSerializer):
    class Meta:
        model = Telephone_bill_call_model
        fields = '__all__'