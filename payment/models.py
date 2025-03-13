from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from comicshop.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime
import logging

logger = logging.getLogger(__name__)


# Create your models here.


class Order(models.Model):
    logger.error(f'***** AN ERROR OCCURRED AT ORDER MODEL')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    shipping_address = models.TextField(max_length=1500)
    amount_paid = models.CharField(max_length=50)
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_shipped = models.DateTimeField(null=True, blank=True)
    shipped = models.BooleanField(default=False)

    def __str__(self):
        return f'Order = {str(self.id)}'


@receiver(pre_save, sender=Order)
def set_shipping_date(sender, instance, **kwargs):
    logger.error(f'***** AN ERROR OCCURRED AT: {instance}')
    if instance.pk:
        now = datetime.datetime.now()
        ob = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not ob.shipped:
            instance.date_shipped = now


class OrderItem(models.Model):
    logger.error(f'***** AN ERROR OCCURRED AT ORDER ITEM MODEL')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.TextField(max_length=50)


class ShippingAddress(models.Model):
    logger.error(f'***** AN ERROR OCCURRED AT SHIPPING ADDRESS MODEL')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255, null=True, default='N/A')
    shipping_postal_code = models.CharField(max_length=20, blank=True, default='N/A')
    shipping_country = models.CharField(max_length=255)

    def __str__(self):
        return f"Shipping Address - {self.user.username}"

    class Meta:
        verbose_name_plural = 'Shipping Addresses'

def create_shipping(sender, instance, created, **kwargs):
    logger.error(f'***** AN ERROR OCCURRED AT: {instance}')
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

post_save.connect(create_shipping, sender=User)

