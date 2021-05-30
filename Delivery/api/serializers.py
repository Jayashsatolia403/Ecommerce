from django.db import models
from rest_framework import serializers

from Delivery.models import Delivery

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = Delivery
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'longitude', 'latitude', 'driving_license', 'password', 'password2']
        extra_kwargs = {'password': {'write_only':True}}
    
    def save(self):
        NewDelivery = Delivery(
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            email = self.validated_data['email'],
            phone = self.validated_data['phone'],
            address = self.validated_data['address'],
            longitude = self.validated_data['longitude'],
            latitude = self.validated_data['latitude'],
            driving_license = self.validated_data['driving_license']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': "Password Must Match."})
        
        NewDelivery.set_password(password)
        NewDelivery.save()
        return NewDelivery
