# serializers.py
from rest_framework import serializers
from .models import Leads, ServicesProvided


class ServicesProvidedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicesProvided
        fields = ['id', 'name']


class LeadsSerializer(serializers.ModelSerializer):
    service_interest = serializers.PrimaryKeyRelatedField(queryset=ServicesProvided.objects.all())

    class Meta:
        model = Leads
        fields = ['id', 'full_name', 'email', 'phone_number', 'service_interest']

    # Optional: Add custom validation for phone_number if needed
    def validate_phone_number(self, value):
        # Add validation logic if necessary
        return value
