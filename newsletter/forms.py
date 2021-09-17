from django import forms
from django.utils.translation import gettext_lazy as _

from newsletter.models import Subscriber


class SubscriptionForm(forms.ModelForm):

    class Meta:
        model = Subscriber
        fields = ('email',)
        widgets = {
            "email": forms.EmailInput(attrs={
                'placeholder': 'Enter Your Email',
                'aria-label': 'Enter Your Email',
                'title': 'Email',
                'type': 'email',
                'aria-required': 'required'
            })
        }
        error_messages = {
            'email': {
                'required': _('Please enter your email'),
                'invalid': _('Enter a valid email'),
                'unique': _('This email is already subscribed')
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'sub-form--input'})
