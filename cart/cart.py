import simplejson as json

from decimal import Decimal
from django.conf import settings

from store.models import Product
from payment.payment import Payment

class Cart():

    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if settings.CART_SESSION_ID not in request.session:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.payment_intent = ''

    def __iter__(self):
        '''
        Get the product_id from the session and query the database for the products
        '''
        products_id = self.cart.keys()
        products = Product.objects.filter(id__in=products_id)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

        print(cart)

    def get_single_product(self, product_id):
        '''
        Get the single / individual product
        '''
        for id, product in self.cart.items():
            if id == str(product_id):
                return {
                    'quantity': product['quantity'] or 0,
                    'id': id or product_id,
                    'price': product['price'] or 0
                }

        # return the only product ID if product has no quantity left
        if str(product_id) not in self.cart.keys():
            return {'id': product_id}

    def total_quantity(self):
        '''
        Get the cart items and total quantity
        '''
        return 0 if not self.cart else sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        '''
        Get the total price of all products in cart
        '''
        return 0 if not self.cart else sum((Decimal(item['price']) * item['quantity']) for item in self.cart.values())

    def add(self, product, quantity):
        '''
        Adding product data to cart session.
        '''
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'price': json.dumps(product.regular_price),
                'quantity': quantity
            }
        else:
            self.cart[product_id]['quantity'] += quantity
            self.payment_intent = self.create_payment_intent()
        self.save()

    def remove(self, product_id, quantity=None, delete=False):
        '''
        Remove one or all product from cart session.
        '''
        product_id = str(product_id)
        if product_id in self.cart:
            if quantity == 1 and not delete:
                qty = self.cart[product_id]['quantity']
                if qty > 1:
                    self.cart[product_id]['quantity'] -= quantity
                else:
                    return
            if delete:
                del self.cart[product_id]
            self.save()
            # self.payment_intent = self.create_payment_intent()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def create_payment_intent(self):
        payment = Payment()
        user_id = self.request.user.pk
        amount = self.get_total_price()
        quantity = self.total_quantity()
        if amount >= 1 and quantity:
            intent = payment.create_payment_intent(
                user_id=user_id, 
                amount=int(str(amount).replace(".", "")), 
                quantity=quantity
            )
            return intent
        else:
            return ''