from orders.models import Order
from django.urls import path

from orders.views import CreateOrder, OrderPlaced, Orders, OrderDetails

app_name = 'order'

urlpatterns = [
    path('your-orders', Orders.as_view(), name="all"),
    path('id/<slug:order_key>', OrderDetails.as_view(), name="details"),
    path('create/', CreateOrder.as_view(), name='create'),
    path('placed/id/<slug:order_key>/', OrderPlaced.as_view(), name='placed'),
]
