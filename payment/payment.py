import stripe

class Payment:

    def create_payment_intent(self, user_id, amount, quantity):
        stripe.api_key = 'sk_test_51HqGZuGM1S732NcONiIrc5W3YMxy8BTPyxXfN8wy6Mx6Q7tolvknT59X8DWhZejEVutudZxVpyBU5FOPEYb6D6OP00WwBcNl5d'
        self.intent = stripe.PaymentIntent.create(
            amount=amount*100,
            currency='inr',
            metadata={
                'user_id': user_id,
                'product_quantity': quantity
            }
        )
        return self.intent