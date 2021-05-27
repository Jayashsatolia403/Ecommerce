from rest_framework import serializers

from Customer.models import Customer

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'city', 'password', 'password2']
        extra_kwargs = {'password': {'write_only':True}}
    
    def save(self):
        NewCustomer = Customer(
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            email = self.validated_data['email'],
            phone = self.validated_data['phone'],
            city = self.validated_data['city'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': "Password Must Match."})
        
        NewCustomer.set_password(password)
        NewCustomer.save()
        return NewCustomer