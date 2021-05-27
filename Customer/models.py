from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from User.models import User


from django.contrib.auth.base_user import BaseUserManager

from rest_framework.authtoken.models import Token
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


class CustomerManager(BaseUserManager):
    def create_cutomer(self, email, first_name, last_name, phone, city, is_verified, password=None):
        if email is None:
            raise TypeError('Customers must have an Email Address!')
        
        if not is_verified:
            raise TypeError('You have not Verified your Email Yet.')

        cutomer = Customer(first_name=first_name, last_name=last_name, email=self.normalize_email(email), phone=phone, city=city)
        cutomer.set_password(password)
        cutomer.save()
        return cutomer

class Customer(User, PermissionsMixin):
    city = models.CharField(max_length=20)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'city']

    objects = CustomerManager()

    def __str__(self):
        return self.email

@receiver(post_save, sender=Customer)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)