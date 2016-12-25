from django.conf.urls import url
from django.conf.urls import include

from rest_framework import routers

from .viewsets import TierViewSet
from .viewsets import OrderViewSet
from .viewsets import PaymentViewSet


router = routers.DefaultRouter()

router.register('tier', TierViewSet, base_name='TierViewSet')
router.register('order', OrderViewSet, base_name='OrderViewSet')
router.register('order/(?P<order__uuid>\d+)', OrderViewSet, base_name='SingleOrderViewSet')
router.register('order/(?P<order__uuid>\w+/purchase)', PaymentViewSet, base_name='CreatePaymentViewSet')


# view_urls = [
#         url(r'order/', OrderViewSet.as_view({'post': 'create'}), name='COrderViewSet'),
# ]

urlpatterns = [
        url(r'^term/', include(router.urls, namespace='api')),
        # url(r'^term/', include(view_urls, namespace='api')),
        ]


