from django.db import models

from Seller.models import Seller



class Category(models.Model):
    title = models.CharField(max_length=255)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, related_name='seller', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    date_added = models.DateTimeField(auto_now_add=True)
    imageone = models.ImageField(upload_to='uploads/', blank=True, null=True)
    imagetwo = models.ImageField(upload_to='uploads/', blank=True, null=True)
    imagethree = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    reviews = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title