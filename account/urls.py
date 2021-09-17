from django.urls import re_path, path, include
from django.contrib.auth import views as auth_views
from django.urls.base import reverse_lazy

from account.views import (
    SignupView, 
    ActivateAccount, 
    signup_success_view, 
    PasswordResetStatus,
)
from account.forms import LoginForm, ResetPasswordForm, NewPasswordForm

app_name = 'account'

urlpatterns = [

    # signup
    path('signup/', SignupView.as_view(), name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/', ActivateAccount.as_view(), name="activate"),
    path('signup/success', signup_success_view, name='signup_success'),

    # login
    path(
        'login/', 
        auth_views.LoginView.as_view(
            template_name='account/login/login.html',
            authentication_form=LoginForm,
            redirect_authenticated_user=True
        ), 
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(next_page='account:login'), name='logout'),

    # reset password
    path('reset-password/', 
        auth_views.PasswordResetView.as_view(
            template_name='account/reset_password/password_reset.html',
            form_class=ResetPasswordForm,
            success_url=reverse_lazy('account:password_reset_sent'),
            email_template_name='account/reset_password/password_reset_email.html'
        ),
        name='reset_password'
    ),
    path('new-password/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='account/reset_password/new_password.html',
            form_class=NewPasswordForm,
            success_url=reverse_lazy('account:password_reset_confirm'),
        ), 
        name='password_reset_form'
    ),
    path("reset-password/sent/", PasswordResetStatus.as_view(), name="password_reset_sent"),
    path("reset-password/confirm/", PasswordResetStatus.as_view(), name="password_reset_confirm"),

    # dashboard
    path('dashboard/', include('dashboard.urls')),
]
