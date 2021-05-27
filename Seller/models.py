from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from User.models import User

from rest_framework.authtoken.models import Token
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

class SellerManager(BaseUserManager):
    def create_seller(self, email, first_name, last_name, phone, address, longitude, latitude, id_proof, is_verified, is_admin_verified, password=None):
        if email is None:
            raise TypeError('Seller must have an Email Address!')
        if id_proof is None:
            raise TypeError('Seller Must have a Valid ID Proof.')

        if not is_verified:
            raise TypeError('You have not Verified Your Email Yet')
        if not is_admin_verified:
            raise TypeError('Admin has not Verified You Identity Yet')

        seller = Seller(first_name=first_name, last_name=last_name, email=self.normalize_email(email), phone=phone, address=address, longitude=longitude, latitude=latitude, id_proof=id_proof)
        seller.set_password(password)
        seller.save()
        return seller

class Seller(User, PermissionsMixin):
    address = models.CharField(max_length=50)
    longitude = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20)
    id_proof = models.ImageField(upload_to='IdProofSeller/', null=True)
    is_admin_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'address', 'longitude', 'latitude', 'id_proof']

    objects = SellerManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=Seller)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)