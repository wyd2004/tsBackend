from django_filters import FilterSet
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response 


from .models import PodcastHost
from .models import PodcastAlbum
from .models import PodcastEpisode
# from .models import PodcastEnclosure

from .serializers import PodcastHostSerializer
from .serializers import PodcastAlbumSerializer
from .serializers import PodcastEpisodeSerializer
# from .serializers import PodcastEnclosureSerializer


class PodcastHostViewSet(viewsets.ModelViewSet):
    model = PodcastHost
    serializer_class = PodcastHostSerializer
    queryset = PodcastHost.objects.all()
    search_fields = ('name',)


class PodcastAlbumViewSet(viewsets.ModelViewSet):
    model = PodcastAlbum
    serializer_class = PodcastAlbumSerializer
    search_fields = ('title',)
    filter_fields = ('hosts__id',)
    ordering_fields = ('-dt_updated',)

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
    ordering_fields = ('-dt_updated',)

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
        return Response()


# class PodcastEnclosureViewSet(viewsets.ModelViewSet):
#     model = PodcastEnclosure
#     serializer_class = PodcastEnclosureSerializer
#     queryset = PodcastEnclosure.objects.all()
#     ordering_fields = ('-dt_updated',)
