from rest_framework import serializers

from Seller.models import Seller
from Product.models import Product

from rest_framework.fields import CurrentUserDefault


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = Seller
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'longitude', 'latitude', 'id_proof', 'password', 'password2']
        extra_kwargs = {'password': {'write_only':True}}
    
    def save(self):
        NewSeller = Seller(
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            email = self.validated_data['email'],
            phone = self.validated_data['phone'],
            address = self.validated_data['address'],
            longitude = self.validated_data['longitude'],
            latitude = self.validated_data['latitude'],
            id_proof = self.validated_data['id_proof'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': "Password Must Match."})
        
        NewSeller.set_password(password)
        NewSeller.save()
        return NewSeller


class AddProductSerializer(serializers.ModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Product
        fields = ['category', 'seller', 'title', 'description', 'price', 'imageone']
    
    def save(self):
        product = Product(
            category = self.validated_data['category'],
            seller = serializers.serialize('json', self.context['request'].user.seller),
            title = self.validated_data['title'],
            description = self.validated_data['description'],
            price = self.validated_data['price'],
            imageone = self.validated_data['imageone']
        )
        
        product.save()
        return product