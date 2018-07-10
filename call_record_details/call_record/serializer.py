from rest_framework import serializers

from .models import Record_model

class Record_serializer(serializers.ModelSerializer):
    class Meta:
        model = Record_model
        fields = '__all__'