import json
from decimal import Decimal
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View

from cart.cart import Cart
from orders.models import Order, OrderItem
from account.models import Customer, Address
from payment.models import Payment




class CreateOrder(View):

    def post(self, request):
        cart = Cart(request)
        body = json.loads(request.body)
        user_id = request.user.id
        amount = cart.get_total_price()

        order_key = body['key']
        address_id = body['addressId']
        customer_id = body['customerId']

        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            customer = Customer.objects.get(id=customer_id)
            address = Address.objects.get(id=address_id)
            order = Order.objects.create(
                user_id=user_id, customer=customer, address=address, amount=amount, order_key=order_key)
            order_id = order.pk
            for item in cart:
                OrderItem.objects.create(
                    order_id=order_id, product=item['product'], price=item['price'], quantity=item['quantity'])

        return JsonResponse({"create": True})



@method_decorator(login_required, name="dispatch")
class OrderPlaced(TemplateView):
    template_name = 'dashboard/order_placed.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        cart.clear()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_key = self.kwargs['order_key']
        order = get_object_or_404(Order, order_key=order_key)
        context['order'] = order
        return context



@method_decorator(login_required, name="dispatch")
class Orders(TemplateView):
    template_name = "dashboard/orders.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
        context['orders'] = orders
        return context



@method_decorator(login_required, name="dispatch")
class OrderDetails(TemplateView):
    template_name = "dashboard/order_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_key = kwargs['order_key']
        context["order"] = get_object_or_404(Order, order_key=order_key)
        return context
    


def payment_confirmation(payment_intent, charge):
    order_key = payment_intent.client_secret
    order = Order.objects.get(order_key=order_key)
    payment = Payment.objects.create(
        user=order.user,
        order=order,
        amount=Decimal(charge.amount / 100),
        client_secret=order_key,
        transaction_id=charge.id,
        payment_intent=charge.payment_intent,
        payment_method=charge.payment_method,
        payment_type=charge.payment_method_details.type,
        payment_created_at=charge.created,
        currency_code=charge.currency,
        card_brand=charge.payment_method_details.card.brand,
        card_country=charge.payment_method_details.card.country,
        card_last_4_digit=charge.payment_method_details.card.last4,
    )
    order.billing_status = True
    order.save()
    payment.save()


def payment_failed():
    pass





