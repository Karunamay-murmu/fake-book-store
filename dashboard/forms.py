from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from django_countries import Countries
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from account.models import Account, Customer, Address


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ("email", "username", "first_name", "last_name",)
        widgets = {
            "username": forms.TextInput(attrs={
                'placeholder': 'Username',
                'aria-label': 'Enter Username',
                'title': 'username',
                'type': 'text',
                'required': True
            }),
            "email": forms.EmailInput(attrs={
                'placeholder': 'Enter Email Address',
                'aria-label': 'Email is readonly',
                'title': 'Email',
                'type': 'email',
                'readonly': 'readonly'
            })
        }
        help_texts = {
            "username": _("Required"),
            "email": _("You can not change email"),
        }
        labels = {
            "username": _('Username'),
            "email": _('Email address'),
            "first_name": _("First name"),
            "last_name": _("Last name")
        }
        error_messages = {
            'username': {
                'required': _('Username is required'),
                'max_length': _('Username is too long'),
                'unique': _("Username aleardy exist")
            },
            'email': {
                'required': _('Email address is required'),
                'invalid': _('Enter valid email')
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'field--input input-username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'field--input input-email'})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'field--input input-first-name'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'field--input input-last-name'})
        # self.request = kwargs['request']




class SelectedCountries(Countries):
    only = [
        'CA', 'FR', 'DE', 'IT', 'JP', 'RU', 'GB',
        ('EU', _('European Union')), 'IN', ('US', _('United State'))
    ]



class AddressForm(forms.ModelForm):

    name = forms.CharField(
        max_length=150,
        required=True,
        label=_("Full name"),
        help_text=_("First and Last name"),
        error_messages={
            "required": _("Enter your full name"),
        },
        widget=forms.TextInput({
            'aria-label': 'Enter Full Name',
            'placeholder': 'Full name',
            'title': 'Full name',
            'type': 'text',
            'class': 'field--input',
            'required': True
        })
    )
    email = forms.EmailField(
        max_length=150,
        required=True,
        label=_("Email"),
        error_messages={
            "required": _("Enter your email address"),
            "invalid": _("Enter a valid email address")
        },        
        widget=forms.EmailInput({
            'aria-label': 'Enter Email Address',
            'placeholder': 'Email address',
            'title': 'Email Address',
            'class': 'field--input',
            'type': 'text',
            'required': True
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        label=_("Phone"),
        help_text=_("10-digit phone number with country code"),
        error_messages={
            "required": _("Enter your phone number"),
        },       
        widget=forms.NumberInput({
            'aria-label': 'Enter Phone Number',
            'placeholder': 'Phone number',
            'title': 'Phone Number',
            'type': 'text',
            'class': 'field--input',
            'required': True
        })
    )
    country = CountryField(countries=SelectedCountries).formfield()

    class Meta:
        model = Address
        fields = ["name", "email", "phone", "address1", "address2",
                  "landmark", "country", "city", "zip_code", "delivery_instruction"]
        widgets = {
            "address1": forms.TextInput(attrs={
                'placeholder': 'Area, Colony, Street',
                'aria-label': 'Enter area, colony, or street',
                'title': 'Area, Colony, Street',
                'type': 'text',
                'required': True
            }),
            "address2": forms.TextInput(attrs={
                'placeholder': 'Flat No, House, Building',
                'aria-label': 'Enter flat no, house, or building',
                'title': 'Flat No, House, Building',
                'type': 'text',
                'required': True
            }),
            "landmark": forms.TextInput(attrs={
                'placeholder': 'E.g Near shopping mall',
                'aria-label': 'Enter landmark',
                'title': 'Landmark',
                'type': 'text',
            }),
            "city": forms.TextInput(attrs={
                'placeholder': 'City or Town',
                'aria-label': 'Enter city or town',
                'title': 'City or Town',
                'type': 'text',
            }),
            "zip_code": forms.TextInput(attrs={
                'placeholder': 'Zip code',
                'aria-label': 'Enter zip code',
                'title': 'Zip code',
                'type': 'text',
            }),
            "delivery_instruction": forms.Textarea(attrs={
                'placeholder': 'Add Delivery Instruction',
                'aria-label': 'Enter delivery instruction',
                'title': 'Delivery instruction',
                'type': 'text',
            }),
        }
        help_texts = {
            "name": _("First and Last name"),
            "phone": _("10-digit phone number with country code"),
            "delivery_instruction": _("(Optional)")
        }
        error_messages = {
            'zip_code': {
                "invalid": _("Enter a valid zip code")
            },
        }
        labels = {
            "address1": _('Area, Colony, Street'),
            "address2": _('Flat No, House, Building'),
            "landmark": _('Landmark'),
            "country": _('Country'),
            "city": _('City or Town'),
            "zip_code": _('Zip Code'),
            "delivery_instruction": _('Delivery Instruction'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address1'].widget.attrs.update(
            {'class': 'field--input'})
        self.fields['address2'].widget.attrs.update(
            {'class': 'field--input'})
        self.fields['landmark'].widget.attrs.update(
            {'class': 'field--input'})
        self.fields['country'].widget.attrs.update(
            {'class': 'field--input'})
        self.fields['city'].widget.attrs.update(
            {'class': 'field--input'})
        self.fields['zip_code'].widget.attrs.update(
            {'class': 'field--input'})
        self.fields['delivery_instruction'].widget.attrs.update(
            {'class': 'field--input'})

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isnumeric():
            raise forms.ValidationError(
                _("Enter a valid phone number")
            )
        return phone




