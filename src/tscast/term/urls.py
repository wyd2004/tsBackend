from django.conf.urls import url
from django.conf.urls import include

from rest_framework import routers

from .viewsets import TierViewSet
from .viewsets import OrderViewSet


router = routers.DefaultRouter()

router.register('term/tier', TierViewSet, base_name='TierViewSet')
router.register('term/order/', OrderViewSet, base_name='OrderViewSet')
router.register('term/order/(?P<order__uuid>\d+)/', OrderViewSet, base_name='OrderViewSet')


urlpatterns = [
        url(r'', include(router.urls, namespace='api')),
        ]
