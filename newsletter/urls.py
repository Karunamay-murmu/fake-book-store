from django.urls import path

from newsletter.views import Subscribe, Unsubscribe

app_name = 'newsletter'

urlpatterns = [
    path('subscribe/', Subscribe.as_view(), name='sub'),
    path('unsubscribe/', Unsubscribe.as_view(), name='unsub')
]


