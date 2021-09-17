from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


from orders.models import Order



class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, related_name='payment')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(_("payment ammont"), max_digits=5, decimal_places=2)
    client_secret = models.CharField(_("client secret"), max_length=255, blank=False, null=True)
    transaction_id = models.CharField(_("transaction id"), max_length=255, blank=False)
    payment_intent = models.CharField(_("payment intent id"), max_length=255, blank=False)
    payment_method = models.CharField(_("payment method id"), max_length=255, blank=False)
    payment_type= models.CharField(_("payment type"), max_length=25, blank=False)
    payment_created_at = models.PositiveIntegerField(_("payment create on"))
    currency_code = models.CharField(_("payment currency code"), max_length=255, blank=False)
    card_brand = models.CharField(_("card brand"), max_length=25, blank=False)
    card_country = models.CharField(_("card country"), max_length=25, blank=False)
    card_last_4_digit = models.CharField(_("card last 4 digit"), max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.transaction_id

    