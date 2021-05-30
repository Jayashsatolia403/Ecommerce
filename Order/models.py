from django.db import models

from Seller.models import Seller
from Customer.models import Customer
from Delivery.models import Delivery
from Product.models import Product

class Order(models.Model):
    address = models.CharField(max_length = 100)
    zipcode = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    longitude = models.CharField(max_length=20, null=True)
    latitude = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    product = models.ManyToManyField(Product, related_name='productOrdered')
    customer = models.ForeignKey(Customer, related_name='customerOfOrder', on_delete=models.CASCADE, null=True)
    seller = models.ForeignKey(Seller, related_name='sellerOfProduct', on_delete=models.CASCADE, null=True)
    delivery = models.ManyToManyField(Delivery, related_name='delivery')
    is_delivered = models.BooleanField(default=False, null=True)
    is_paid = models.BooleanField(default=False, null=True)

    class Meta:
        ordering = ['-created_at']