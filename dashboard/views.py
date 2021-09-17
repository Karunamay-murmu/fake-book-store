from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy, reverse

from dashboard.forms import EditProfileForm, AddressForm
from account.models import Account, Address, Customer
from orders.models import Order
from store.models import Product, ProductSpecification, ProductSpecificationValue



@method_decorator(login_required, name="dispatch")
class DashboardIndexView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
        context['orders'] = orders
        return context



@method_decorator(login_required, name="dispatch")
class EditProfile(UpdateView):
    form_class = EditProfileForm
    model = Account
    template_name = 'dashboard/edit_profile.html'
    success_url = reverse_lazy('account:profile:dashboard')


    def get_object(self):
        username = self.kwargs['username']
        user = get_object_or_404(Account, username=username)
        return user

    # def form_invalid(self, form):
    #     print(form.errors)
    #     return super().form_invalid(form)

    # def get_form_kwargs(self):
    #     kwargs = super(EditProfile, self).get_form_kwargs()
    #     return kwargs




@login_required
def delete_profile(request):
    user = Account.objects.get(username=request.user)
    user.is_active = False
    user.save()
    logout(request)
    messages.success(request, 'Account has been deleted')
    return redirect('store:index')



@method_decorator(login_required, name="dispatch")
class AddressView(TemplateView):

    template_name = "dashboard/address.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        addresses = Address.objects.filter(customer__account=user)
        context['addresses'] = addresses
        return context



@method_decorator(login_required, name="dispatch")
class AddressActionView(View):
    template_name = 'dashboard/address_form.html'
    form_class = AddressForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print(request.META['QUERY_STRING'])
        if not request.GET['action'] == 'add':
            id = request.GET['id']
            address = Address.objects.filter(pk=id, customer__account=request.user)

        if request.GET['action'] == "edit":
            address = Address.objects.get(pk=id, customer__account=request.user)
            customer = address.customer
            initial = {
                'name': customer.name,
                'email': customer.email,
                'phone': customer.phone,
            }
            form = self.form_class(initial=initial, instance=address)

        if request.GET['action'] == 'delete':
            address.delete()
            return redirect("account:profile:show_address")

        if request.GET['action'] == 'set_default':
            Address.objects.filter(customer__account=request.user, default=True).update(default=False)
            address.update(default=True)
            return redirect(request.META['HTTP_REFERER'])

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        action = request.GET['action']
        if action == 'add':
            form = self.form_class(request.POST)

        if action == 'edit':
            id = request.GET['id']
            address = Address.objects.get(pk=id, customer__account=request.user)
            form = self.form_class(instance=address, data=request.POST)

        if form.is_valid():
            address = form.save(commit=False)

            # creating  a customer
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']

            customer, created = Customer.objects.update_or_create(
                email=email,
                defaults={
                    'name':name,
                    'email': email,
                    'phone':phone,
                    'account': request.user
                }
            )
            customer.save()

            if created:
                address.customer = customer

            address.save()
            messages.success(request, "Address saved successfully")

            return HttpResponseRedirect(reverse("account:profile:show_address"))

        return render(request, self.template_name, {'form': form})



class WishlistView(TemplateView):
    template_name = "dashboard/wishlist.html"

    def get_context_data(self):
        context = super().get_context_data()
        products = Product.objects.filter(wishlist=self.request.user)
        context['products'] = products
        return context



@method_decorator(login_required, name="dispatch")
class AddToWishList(View):

    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        if product.wishlist.filter(id=request.user.id).exists():
            product.wishlist.remove(request.user)
            messages.success(request, f"{product.title} remove from your wishlist")
        else:
            product.wishlist.add(request.user)
            messages.success(request, f"{product.title} added to your wishlist")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
