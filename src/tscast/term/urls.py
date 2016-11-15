from django.conf.urls import url
from django.conf.urls import include

from rest_framework import routers

from .viewsets import TierViewSet


router = routers.DefaultRouter()

router.register('podcast/tangsuan/term/tier', TierViewSet, base_name='TierViewSet')


urlpatterns = [
        url(r'', include(router.urls, namespace='api')),
        ]
