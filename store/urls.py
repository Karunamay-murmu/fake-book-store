from django.urls import path, re_path
from django.conf.urls.static import static

from store.views import Home, ProductDetail, Shop, Search

app_name="store"

urlpatterns = [
    path('', Home.as_view(), name="index"),
    path('shop/', Shop.as_view(), name="shop"),
    path('shop/<slug:type>/<slug:slug>/', ProductDetail.as_view(), name="product_detail"),
    path('shop/search/', Search.as_view(), name="search")
]