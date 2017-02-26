from django.conf.urls import url
from django.conf.urls import include

from rest_framework import routers

from .viewsets import PodcastAlbumSubscriptionViewSet, PodcastEpisodeSubscribeViewSet
from .viewsets import PodcastAlbumSubscribeViewSet
from .viewsets import PodcastEpisodeSubscriptionViewSet
from .viewsets import MemberPurchasedAlbumViewSet 
from .viewsets import MemberViewSet 
from .viewsets import oauth
from .viewsets import invitation_activate
from rest_framework.authtoken import views

router = routers.DefaultRouter()

router.register('member', MemberViewSet, base_name='MemberViewSet')
router.register('member/(?P<member_id>\d+)/subscription/album',PodcastAlbumSubscriptionViewSet, base_name='PodcastAlbumSubscriptionViewSet')
router.register('member/(?P<member_id>\d+)/subscription/episode',PodcastEpisodeSubscriptionViewSet, base_name='PodcastEpisodeSubscriptionViewSet')
router.register('member/(?P<member_id>\d+)/purchase/album', MemberPurchasedAlbumViewSet, base_name='MemberPurchasedAlbumViewSet')


view_urls = [
        url('podcast/album/(?P<album_id>\d+)/subscribe/',
            PodcastAlbumSubscribeViewSet.as_view(
                {'post': 'create', 'delete': 'destroy'}
                ),
            name='PodcastAlbumSubscribeViewSet',
            ),
        url('podcast/episode/(?P<album_id>\d+)/subscribe/',
            PodcastEpisodeSubscribeViewSet.as_view(
                {'post': 'create', 'delete': 'destroy'}
                ),
            name='PodcastEpisodeSubscribeViewSet',
            ),
        url('member/oauth/', oauth, name='member-oauth'),
        url('^api-token-auth/', views.obtain_auth_token),
        url('member/invitation/activate/(?P<key>[\w\d-]+)/', invitation_activate, name='invitation-activate'),
        ]


urlpatterns = [
        url(r'', include(view_urls, namespace='api')),
        url(r'', include(router.urls, namespace='api')),
        ]
