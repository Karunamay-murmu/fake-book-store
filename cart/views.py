import json

from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from django.views import View

from cart.cart import Cart
from store.models import Product
from account.models import Address


class CartView(TemplateView):
    template_name = "cart/cart.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if not user.is_anonymous:
            addresses = Address.objects.filter(customer__account=user)
            context['addresses'] = addresses

        return context


class AddToCartView(View):

    def get(self, request, *args, **kwargs):
        '''
        Add the product information and quantity to cart session.
        '''
        cart = Cart(request)
        product_id = int(request.GET['productId'])
        quantity = int(request.GET['quantity'])
        product = get_object_or_404(Product, id=product_id)
        cart.add(
            product=product,
            quantity=quantity
        )

        return JsonResponse({
            'total_quantity':  f"{cart.total_quantity()}",
            'product': cart.get_single_product(product_id),
            'total_price': cart.get_total_price(),
            'payment_intent_client_key': cart.payment_intent['client_secret'] if cart.payment_intent and cart.payment_intent != '' else ''
        })


class DeleteFromCartView(View):

    def get(self, request, *args, **kwargs):
        '''
        Delete the product information and quantity from cart session.
        '''
        cart = Cart(request)
        product_id = int(request.GET.get('productId', ''))
        quantity = int(request.GET.get('quantity', 0))
        delete = request.GET.get('delete', None)

        cart.remove(product_id=product_id, quantity=quantity, delete=delete)

        return JsonResponse({
            'total_quantity':  cart.total_quantity(),
            'product': cart.get_single_product(product_id),
            'total_price': cart.get_total_price(),
        })
