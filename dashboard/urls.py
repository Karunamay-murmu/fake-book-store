from django.urls import path, re_path

from dashboard.views import (
    DashboardIndexView, 
    EditProfile, 
    delete_profile,
    AddressView,
    AddressActionView,
    WishlistView,
    AddToWishList
)

app_name = 'profile'

urlpatterns = [
    path('', DashboardIndexView.as_view(), name="dashboard"),
    path('<slug:username>/edit-profile', EditProfile.as_view(), name="edit_profile"),
    path('<slug:username>/delete-profile', delete_profile, name="delete-profile"),

    # address
    path('your_address/', AddressView.as_view(), name="show_address"),
    path('address/', AddressActionView.as_view(), name="edit_address"),

    # wishlist
    path('your_wistlist/', WishlistView.as_view(), name="wishlist"),
    path('wishlist/add/<int:id>/', AddToWishList.as_view(), name="add_wishlist")
]
