import stripe
import json

from django.http import JsonResponse, HttpResponse, request
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt

from cart.cart import Cart
from payment.payment import Payment
from orders.views import payment_confirmation, payment_failed



@method_decorator(login_required, name="dispatch")
class CartPaymentIntentView(View):

    def get(self, request):
        cart = Cart(request)
        payment = Payment()
        user_id = request.user.pk
        amount = int(cart.get_total_price())
        quantity = cart.total_quantity()
        intent = payment.create_payment_intent(user_id=user_id, amount=amount, quantity=quantity)
        return JsonResponse({'secret_key': intent['client_secret']})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError as e:
        return HttpResponse(status=400)

    # Handle the event
    if event.type == "payment_intent.succeeded":
        payment_intent = event.data.object
        charge = event.data.object.charges.data[0]
        payment_confirmation(payment_intent, charge)
    else:
        payment_failed()
        print('unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)


