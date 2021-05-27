from Product.models import Product
from django.db import models

from Customer.models import Customer

class Cart(models.Model):
    customer = models.OneToOneField(Customer, related_name='customer', on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    total = models.IntegerField()