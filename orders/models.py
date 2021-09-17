from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from store.models import Product
from account.models import Customer, Address



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order")
    customer = models.ForeignKey(Customer, related_name="order", on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.created_at)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_item")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_product")
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

