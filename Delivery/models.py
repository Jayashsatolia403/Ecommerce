from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from User.models import User

from rest_framework.authtoken.models import Token
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


class DeliveryManager(BaseUserManager):
    def create_delivery(self, email, first_name, last_name, phone, address, longitude, latitude, driving_licence, is_verified, is_admin_verified, password=None):
        if email is None:
            raise TypeError('Delivery Agent must have an Email Address!')
        if driving_licence is None:
            raise TypeError('Delivery Agent Must have a Driving Licence.')

        if not is_verified:
            raise TypeError('You have not Verified Your Email Yet')
        if not is_admin_verified:
            raise TypeError('Admin has not Verified You Identity Yet')

        delivery = Delivery(first_name=first_name, last_name=last_name, email=self.normalize_email(email), phone=phone, address=address, longitude=longitude, latitude=latitude, driving_licence=driving_licence)
        delivery.set_password(password)
        delivery.save()
        return delivery

class Delivery(User, PermissionsMixin):
    address = models.CharField(max_length=50)
    longitude = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20)
    driving_license = models.ImageField(upload_to='DrivingLicenseDelivery/', null=True)
    is_admin_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'address', 'longitude', 'latitude', 'driving_licence']

    objects = DeliveryManager()

    def __str__(self):
        return self.email

@receiver(post_save, sender=Delivery)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)