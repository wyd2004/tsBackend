from django_filters import FilterSet
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response 
from django.http.response import HttpResponseRedirect


from .models import PodcastHost
from .models import PodcastAlbum
from .models import PodcastEpisode
# from .models import PodcastEnclosure

from .serializers import PodcastHostSerializer
from .serializers import PodcastAlbumSerializer
from .serializers import PodcastEpisodeSerializer
# from .serializers import PodcastEnclosureSerializer

from tscast.utils.permissions import ReadOnly
from member.utils.permissions import OnlyMemberAccess


class PodcastHostViewSet(viewsets.ModelViewSet):
    model = PodcastHost
    serializer_class = PodcastHostSerializer
    permission_classes = (ReadOnly, OnlyMemberAccess)
    queryset = PodcastHost.objects.all()
    search_fields = ('name',)


class PodcastAlbumViewSet(viewsets.ModelViewSet):
    model = PodcastAlbum
    serializer_class = PodcastAlbumSerializer
    permission_classes = (ReadOnly, OnlyMemberAccess)
    search_fields = ('title', 'keywords')
    filter_fields = ('hosts__id', 'is_hot')
    ordering_fields = ('is_hot', 'dt_updated', 'id', 'title')
    ordering = ('-dt_updated',)

    def get_queryset(self):
        queryset = self.model.objects.filter(
                is_deleted=False,
                status='publish',
                )
        if 'hosts__id' in self.kwargs:
            queryset = queryset.filter(hosts__id=self.kwargs['hosts__id'])
        return queryset


class PodcastEpisodeViewSet(viewsets.ModelViewSet):
    model = PodcastEpisode
    serializer_class = PodcastEpisodeSerializer
    permission_classes = (ReadOnly, OnlyMemberAccess)
    search_fields = ('title',)
    ordering_fields = ('dt_updated', 'id')
    ordering = ('-dt_updated',)

    def get_queryset(self):
        queryset = self.model.objects.filter(
                is_deleted=False,
                status='publish',
                )
        if 'hosts__id' in self.kwargs:
            queryset = queryset.filter(hosts__id=self.kwargs['hosts__id'])
        return queryset

    def get_next(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            next_obj = obj.get_next_by_dt_created()
        except self.model.DoesNotExist as error:
            raise NotFound
        data = self.serializer_class(next_obj).data
        return Response(data)

    def get_previous(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            previous_obj = obj.get_next_by_dt_created()
        except self.model.DoesNotExist as error:
            raise NotFound
        data = self.serializer_class(previous_obj).data
        return Response(data)

    def get_earlier(self, request, *args, **kwargs):
        obj = self.get_object()
        queryset = self.get_queryset().filter(
                album=obj.album,
                dt_created__lte=obj.dt_created,
                status='publish',
                is_deleted=False).exclude(
                id=obj.id)
        self.get_queryset = lambda: queryset
        return self.list(self, request, *args, **kwargs)

    def get_full_file(self, request, *args, **kwargs):
        obj = self.get_object()
        # data = {'full_url': 'http://xx.mp3'}
        # return Response(data)
        url = 'http://cdn5.lizhi.fm/audio/2016/11/25/2570200503485179398_hd.mp3'
        return HttpResponseRedirect(url)

    def get_preview_file(self, request, *args, **kwargs):
        obj = self.get_object()
        # data = {'full_url': 'http://xx.mp3'}
        # return Response(data)
        url = 'http://cdn5.lizhi.fm/audio/2016/11/25/2570200503485179398_hd.mp3'
        return HttpResponseRedirect(url)


    def get_serializer_context(self):
        return {'request': self.request}


# class PodcastEnclosureViewSet(viewsets.ModelViewSet):
#     model = PodcastEnclosure
#     serializer_class = PodcastEnclosureSerializer
#     queryset = PodcastEnclosure.objects.all()
#     ordering_fields = ('-dt_updated',)
