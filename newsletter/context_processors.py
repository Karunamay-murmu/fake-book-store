from newsletter.forms import SubscriptionForm

def newsletter(request):
    return {'subscription_form': SubscriptionForm()}
