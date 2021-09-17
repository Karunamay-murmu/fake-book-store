from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _

from account.models import Account


class SignupForm(forms.ModelForm):

    password = forms.CharField(
        min_length=6,
        required=True,
        label='Password',
        help_text=_('minimum 6 characters long'),
        widget=forms.PasswordInput(attrs={
            'aria-label': 'Enter password',
            'placeholder': '••••••',
            'title': 'Password',
            'type': 'password',
            'required': True
        }),
        error_messages={
            'required': _('Password is required'),
            'min_length': _('Password is too short')
        }
    )

    password2 = forms.CharField(
        required=True,
        label='Confirm password',
        widget=forms.PasswordInput(attrs={
            'aria-label': 'Confirm password',
            'placeholder': '••••••',
            'title': 'Confirm password',
            'type': 'password',
            'required': True
        }),
        error_messages={
            'required': _('Re-Enter Your Password'),
        }
    )

    class Meta:
        model = Account
        fields = ("username", "email",)
        widgets = {
            "username": forms.TextInput(attrs={
                'placeholder': 'Username',
                'aria-label': 'Enter Username',
                'title': 'username',
                'type': 'text',
                'required': True
            }),
            "email": forms.EmailInput(attrs={
                'placeholder': 'Email',
                'aria-label': 'Enter Email Address',
                'title': 'Email',
                'type': 'email',
                'required': True
            })
        }
        help_texts = {
            "username": _("Required"),
            "email": _("Required"),
        }
        labels = {
            "username": _('Username'),
            "email": _('Email address'),
        }
        error_messages = {
            'username': {
                'required': _('Username is required'),
                'max_length': _('Username is too long'),
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
        self.fields['password'].widget.attrs.update(
            {'class': 'field--input input-password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'field--input input-confirm-password'})

    def clean_username(self):
        username = self.cleaned_data['username']
        user = Account.objects.filter(username=username)
        if user.count():
            raise forms.ValidationError(
                _("Username already exist"), code='invalid')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        email_exist = Account.objects.filter(email=email).exists()
        if email_exist:
            raise forms.ValidationError(
                _("Email already exist"), code='invalid')
        return email

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError(
                _("Passwords do not match"), code="invalid")
        return data['password2']


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label=_('Email Address'),
                                required=True,
                                widget=forms.EmailInput(attrs={
                                    'class': 'field--input input--email',
                                    'type': 'email',
                                    'aria-label': 'enter your email',
                                    'placeholder': 'Email',
                                    'title': 'Email',
                                }))
    password = forms.CharField(label=_("Password"),
                               required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'field--input input--password',
                                   'type': 'password',
                                   'aria-label': 'enter your password',
                                   'placeholder': '••••••',
                                   'title': 'Password'
                               }))

    error_messages = {
        'invalid_login': _(
            "Email address and password didn't match."
        ),
        'inactive': _("This account is not active."),
    }


class ResetPasswordForm(PasswordResetForm):
    email = forms.CharField(max_length=254, label="Email Address", widget=forms.EmailInput(
        attrs={
            'class': 'field--input input-reset-password',
            'placeholder': 'Enter Your Email',
            'required': True,
            'id': 'id_reset-password',
            'aria-label': 'Enter Your Email',
            'autocomplete': 'email'
        }),
        error_messages={
            'required': _('Please enter your email'),
        }
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        user = Account.objects.filter(email=email)
        if not user:
            raise forms.ValidationError(
                _('Account cannot be found with %s that email.' % (email)),
                code='invalid'
            )
        return email


class NewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        help_text='minimum 6 characters long.',
        min_length=6,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'field--input input-new-password',
                'placeholder': 'Enter New Password',
                'required': True,
                'id': 'id_new-password',
                'aria-label': 'Enter New Password',
                'autofocus': True
            }),
        error_messages={
            'required': _('Please enter a new password'),
            'min_length': _('Password is too short')
        }
    )
    new_password2 = forms.CharField(
        label=_("Confirm New password"),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'field--input input-confirm-new-password',
                'placeholder': 'Re-Enter Password',
                'required': True,
                'id': 'id_confirm-new-password',
                'aria-label': 'Re-Enter Password',
            }),
        error_messages={
            'required': _('Re-Enter the password once again.'),
        }
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        else:
            return password2