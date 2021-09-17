from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy


from account.forms import SignupForm
from account.models import Account
from account.token import token
from store.models import Product



class UserLoginMixin():
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            messages.success(request, 'You already Log in')
            return redirect('account:profile:dashboard')
        return super().get(request)



class SignupView(UserLoginMixin, CreateView):
    form_class = SignupForm
    model = Account
    template_name = "account/signup/signup.html"
    success_url = reverse_lazy('account:signup_success')

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()

        # setup email
        current_site = get_current_site(self.request)
        subject = 'Activate Your Account'
        message = render_to_string(
            'account/signup/activation_email.html',
            {
                'user': user,
                'domain': current_site.domain,
                'user_id': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token.make_token(user)
            }
        )
        send_mail(subject=subject, message=message,
                  from_email='no-reply@django.com', recipient_list=[user.email])
        return super().form_valid(form)



class ActivateAccount(View):

    def get(self, request, *args, **kwargs):
        user_id = force_text(urlsafe_base64_decode(kwargs['uidb64']))
        if user_id:
            user = Account.objects.get(pk=user_id)
            activation_token = token.check_token(user, kwargs['token'])
            if user is not None and activation_token:
                user.is_active = True
                user.save()
                return redirect('account:profile:dashboard')
            else:
                return render(request, 'account/signup/activation_invalid.html')
        else:
            ...



def signup_success_view(request):
    if request.method == "GET":
        user = request.user
        if user.is_authenticated or user.is_active:
            return redirect("/")
        return render(request, 'account/signup/signup_success.html')



class PasswordResetStatus(TemplateView):
    template_name = 'account/reset_password/reset_status.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('account:profile:dashboard')
        return super().get(request)



