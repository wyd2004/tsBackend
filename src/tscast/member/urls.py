from django.conf.urls import url
from django.conf.urls import include

from rest_framework import routers

from .viewsets import PodcastAlbumSubscriptionViewSet
from .viewsets import PodcastAlbumSubscribeViewSet
from .viewsets import MemberPurchasedAlbumViewSet 
from .viewsets import oauth


router = routers.DefaultRouter()

router.register('member/(?P<member_id>\d+)/subscription',PodcastAlbumSubscriptionViewSet, base_name='PodcastAlbumSubscriptionViewSet')
router.register('member/(?P<member_id>\d+)/purchase', MemberPurchasedAlbumViewSet, base_name='PodcastAlbumSubscriptionViewSet')


view_urls = [
        url('podcast/tangsuan/album/(?P<album_id>\d+)/subscribe/',
            PodcastAlbumSubscribeViewSet.as_view(
                {'post': 'create', 'delete': 'destroy'}
                ),
            name='PodcastAlbumSubscribeViewSet',
            ),
        url('member/oauth/', oauth, name='member-oauth'),
        ]


urlpatterns = [
        url(r'', include(view_urls, namespace='api')),
        url(r'', include(router.urls, namespace='api')),
        ]
