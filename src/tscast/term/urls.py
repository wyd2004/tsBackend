from django.conf.urls import url
from django.conf.urls import include

from rest_framework import routers

from .viewsets import TierViewSet
from .viewsets import OrderViewSet
from .viewsets import payment_callback


router = routers.DefaultRouter()

router.register('term/tier', TierViewSet, base_name='TierViewSet')
router.register('term/order', OrderViewSet, base_name='OrderViewSet')


urlpatterns = [
        url(r'', include(router.urls, namespace='api')),
        url(r'^term/payment/(?P<uuid>[\w-]+?)/callback/', payment_callback, name='payment_callback')
        ]
