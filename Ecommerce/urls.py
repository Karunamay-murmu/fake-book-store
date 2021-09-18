import debug_toolbar

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from Ecommerce.settings import core_settings as settings

urlpatterns = [
    path('', include('store.urls')),
    path('category/', include('category.urls')),
    path('cart/', include('cart.urls')),
    path('user/', include('account.urls')),
    path('payment/', include('payment.urls')),
    path('order/', include('orders.urls')),
    path('newsletter/', include('newsletter.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG == True:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
