from django.conf.urls import url
from django.conf.urls import include

from rest_framework import routers

from .viewsets import PodcastAlbumSubscriptionViewSet
from .viewsets import PodcastAlbumSubscribeViewSet
from .viewsets import MemberPurchasedAlbumViewSet 
from .viewsets import MemberViewSet 
from .viewsets import oauth
from .viewsets import active_trial_key

router = routers.DefaultRouter()

router.register('member', MemberViewSet, base_name='MemberViewSet')
router.register('member/(?P<member_id>\d+)/subscription/album',PodcastAlbumSubscriptionViewSet, base_name='PodcastAlbumSubscriptionViewSet')
router.register('member/(?P<member_id>\d+)/purchase/album', MemberPurchasedAlbumViewSet, base_name='PodcastAlbumSubscriptionViewSet')


view_urls = [
        url('podcast/album/(?P<album_id>\d+)/subscribe/',
            PodcastAlbumSubscribeViewSet.as_view(
                {'post': 'create', 'delete': 'destroy'}
                ),
            name='PodcastAlbumSubscribeViewSet',
            ),
        url('member/oauth/', oauth, name='member-oauth'),
        url('member/active/(?P<key>[\w\d-]+)/', active_trial_key, name='trial-member-active'),
        ]


urlpatterns = [
        url(r'', include(view_urls, namespace='api')),
        url(r'', include(router.urls, namespace='api')),
        ]
