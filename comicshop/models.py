from django.db import models
import shortuuid
from djmoney.models.fields import MoneyField
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

import logging

logger = logging.getLogger(__name__)
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=100, blank=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True)
    old_cart = models.CharField(max_length=500, blank=True, null=True)

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)

class Category(models.Model):

    name = models.CharField(max_length=50)
    logger.error(f'***** AN ERROR OCCURED at CATEGORY MODEL')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Categories'


class Customer(models.Model):
    logger.error(f'***** AN ERROR OCCURED at CUSTOMER MODEL')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.EmailField()
    password = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Product(models.Model):
    logger.error(f'***** AN ERROR OCCURED at PRODUCT MODEL')
    artist_name = models.CharField(max_length=50)
    publisher = models.ForeignKey(Category, on_delete=models.CASCADE)
    comics = models.TextField()
    work_link = models.URLField()
    stock_number = models.CharField(shortuuid.ShortUUID().random(length=6), max_length=6)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    image = models.ImageField(upload_to='upload/products')
    image1 = models.ImageField(upload_to='upload/products', null=True, blank=True)
    image2 = models.ImageField(upload_to='upload/products', null=True, blank=True)
    image3 = models.ImageField(upload_to='upload/products', null=True, blank=True)
    image4 = models.ImageField(upload_to='upload/products', null=True, blank=True)
    image5 = models.ImageField(upload_to='upload/products', null=True, blank=True)
    image6 = models.ImageField(upload_to='upload/products', null=True, blank=True)
    image7 = models.ImageField(upload_to='upload/products', null=True, blank=True)
    image8 = models.ImageField(upload_to='upload/products', null=True, blank=True)
    
    

