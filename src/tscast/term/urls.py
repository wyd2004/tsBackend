from django.conf.urls import url
from django.conf.urls import include

from rest_framework import routers

from .viewsets import TierViewSet
from .viewsets import OrderViewSet


router = routers.DefaultRouter()

router.register('tier', TierViewSet, base_name='TierViewSet')
router.register('order', OrderViewSet, base_name='OrderViewSet')
router.register('order/(?P<order__uuid>\d+)', OrderViewSet, base_name='SingleOrderViewSet')


urlpatterns = [
        url(r'^term/', include(router.urls, namespace='api')),
        ]
