from django.urls import path

from cart.views import CartView, AddToCartView, DeleteFromCartView

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/', AddToCartView.as_view(), name='add'),
    path('delete/', DeleteFromCartView.as_view(), name='delete')
]
