from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.contrib import messages

from newsletter.models import Subscriber
from newsletter.forms import SubscriptionForm



class Subscribe(View):

    def post(self, request):
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = request.POST.get('sub_email')
            is_subscriber = Subscriber.objects.filter(
                email__iexact=email).exists()
            if not is_subscriber:
                Subscriber.objects.create(email=email)
                context = {'new_subscriber': True}
            else:
                context = {'new_subscriber': False}
            return render(request, 'newsletter/subscribe.html', context)
        else:
            error = form.errors['email'][0]
            messages.error(request, '%s' %error)
            return redirect(request.META['HTTP_REFERER'])


class Unsubscribe(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('unsub')
