from django.urls import path

from payment.views import CartPaymentIntentView, stripe_webhook

app_name = 'payment'

urlpatterns = [
    path('', CartPaymentIntentView.as_view(), name='intent'),
    path('stripe-hook/', stripe_webhook),
]
