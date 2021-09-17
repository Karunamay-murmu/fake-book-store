import uuid

from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django_countries import Countries

from django_countries.fields import CountryField



class AccountManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password=None):
        if not email:
            raise ValueError(_("User must have an email address"))
        if not username:
            raise ValueError(_("User must have an username"))
        if not first_name:
            raise ValueError(_("User must have an first_name"))
        if not last_name:
            raise ValueError(_("User must have an last_name"))

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, first_name, last_name, email, password=None):
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)

        return user
        


class Account(AbstractBaseUser):
    first_name = models.CharField(_("first name"), max_length=50, blank=True)
    last_name = models.CharField(_("last name"), max_length=50, blank=True)
    username = models.CharField(_("username"), max_length=10, unique=True, blank=False, null=False)
    email = models.EmailField(_("email address"), unique=True, blank=False, null=False)

    date_joined = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"



class Customer(models.Model):

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="customer", related_query_name="account", default=Account)
    name = models.CharField(_("customer's full name"), max_length=150, blank=False)
    email = models.EmailField(_("customer's email address"), max_length=150, unique=True)
    phone = models.CharField(_("customer's phone number"), max_length=20, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.name



class Address(models.Model):

    # Customer's address TABLE
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="address", related_query_name="customer")
    address1 = models.CharField(_('area, colony, street'), max_length=255, blank=False, null=True)
    address2 = models.CharField(_('flat, house, building'), max_length=255, blank=False, null=True)
    landmark = models.CharField(_("landmark"), max_length=255, null=True)
    country = CountryField()
    city=models.CharField(_("city or town"), max_length=50, blank=False, null=False)
    zip_code = models.IntegerField(_("area zip code"), blank=False, null=False)
    delivery_instruction = models.CharField(_("delivery instruction"), max_length=255, blank=True)
    default = models.BooleanField(_("default"), default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.address1