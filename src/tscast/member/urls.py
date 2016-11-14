from django.conf.urls import url
from django.conf.urls import include

from rest_framework import routers

from .viewsets import PodcastAlbumSubscriptionViewSet
from .viewsets import PodcastAlbumSubscribeViewSet


router = routers.DefaultRouter()

router.register('member/(?P<member_id>\d+)/album_subscription', PodcastAlbumSubscriptionViewSet, base_name='PodcastAlbumSubscriptionViewSet')

view_urls = [
        url('podcast/tangsuan/album/(?P<album_id>\d+)/subscribe/',
            PodcastAlbumSubscribeViewSet.as_view(
                {'post': 'create', 'delete': 'destroy'}
                ),
            name='PodcastAlbumSubscribeViewSet',
            )
        ]


urlpatterns = [
        url(r'', include(view_urls, namespace='api')),
        url(r'', include(router.urls, namespace='api')),
        ]
