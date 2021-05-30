import vincenty

from rest_framework import serializers

from Order.models import Order
from Delivery.models import Delivery

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['address', 'zipcode', 'phone', 'longitude', 'latitude']
    
    def save(self):
        global i
        NewOrder = Order(
            customer = self.context['request'].user.customer,
            zipcode = self.validated_data['zipcode'],
            address = self.validated_data['address'],
            phone = self.validated_data['phone'],
            longitude = self.validated_data['longitude'],
            latitude = self.validated_data['latitude'],
            seller = self.context['sellerOfProduct']
        )
        
        NewOrder.save()

        deliveryForOrders = Delivery.objects.all()
        for deliveryForOrder in deliveryForOrders:
            distance = vincenty.vincenty((float(deliveryForOrder.longitude), float(deliveryForOrder.latitude)), (float(self.validated_data['longitude']), float(self.validated_data['latitude'])))
            if distance < 20:
                NewOrder.delivery.add(deliveryForOrder)

        NewOrder.product.add(self.context['orderedProduct'])

        
        
        return NewOrder