from django.conf.urls import url
from django.conf.urls import include

from rest_framework import routers

from .viewsets import PodcastHostViewSet
from .viewsets import PodcastAlbumViewSet
from .viewsets import PodcastEpisodeViewSet
# from .viewsets import PodcastEnclosureViewSet


router = routers.DefaultRouter()
router.register('people', PodcastHostViewSet, base_name='PodcastPeopleViewSet')
router.register('people/(?P<hosts__id>\d+)/album', PodcastAlbumViewSet, base_name='PeoplePodcastAlbumViewSet')
router.register('people/(?P<hosts__id>\d+)/episode', PodcastEpisodeViewSet, base_name='PeoplePodcastEpisodeViewSet')
router.register('album', PodcastAlbumViewSet, base_name='PodcastAlbumViewSet')
router.register('album/(?P<album>\d+)/episode', PodcastEpisodeViewSet, base_name='AlbumPodcastEpisodeViewSet')
router.register('episode', PodcastEpisodeViewSet, base_name='PodcastEpisodeViewSet')


view_urls = [
        url(r'episode/(?P<pk>\d+)/next/', PodcastEpisodeViewSet.as_view({'get': 'get_next'}), name='NextPodcastEpisodeViewSet'),
        url(r'episode/(?P<pk>\d+)/previous/', PodcastEpisodeViewSet.as_view({'get': 'get_previous'}), name='PreviousPodcastEpisodeViewSet')
        ]
        

urlpatterns = [
        url(r'^podcast/', include(view_urls, namespace='api')),
        url(r'^podcast/', include(router.urls, namespace='api')),
    ]
