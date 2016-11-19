from django_filters import FilterSet
from django.db.models import Count
from rest_framework import viewsets
from rest_framework import views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import BasePermission


from .models import PodcastAlbumSubscription
from .models import Member
from .models import MemberToken

from .serializers import PodcastAlbumSubscriptionSerializer
from .serializers import PodcastAlbumSubscribeSerializer


from podcast.viewsets import PodcastAlbumViewSet



@api_view(['GET', 'HEAD'])
def oauth(request, format='json'):
    token = MemberToken.objects.first()
    data = {'token': token.key, 'member_id': token.user.id}
    response = Response(data)
    return response


class PodcastAlbumSubscriptionViewSet(viewsets.ModelViewSet):
    model = PodcastAlbumSubscription
    serializer_class = PodcastAlbumSubscriptionSerializer
    filter_fields = ('member_id',)

    def get_queryset(self):
        queryset = PodcastAlbumSubscription.objects.filter(is_deleted=False)
        if self.kwargs.has_key('member_id'):
            queryset = queryset.filter(member_id=self.kwargs['member_id'])
        return queryset


class PodcastAlbumSubscribePermission(BasePermission):
    def has_permission(self, request, view):
        if type(request.user) == Member:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return False


class PodcastAlbumSubscribeViewSet(viewsets.ModelViewSet):
    model = PodcastAlbumSubscription
    serializer_class = PodcastAlbumSubscribeSerializer
    permission_classes = (PodcastAlbumSubscribePermission,)


    def get_queryset(self):
        queryset = PodcastAlbumSubscription.objects.filter(is_deleted=False)
        return queryset

    def create(self, request, *args, **kwargs):
        obj = self.model.objects.filter(
                album_id=kwargs.get('album_id', 0),
                member=request.user,
                is_deleted=False
                ).last()
        if obj:
            data = self.serializer_class(instance=obj).data
            return Response(data)
        else:
            return super(PodcastAlbumSubscribeViewSet, self).create(request, *args, **kwargs)


    def destroy(self, request, *args, **kwargs):
        queryset = self.model.objects.filter(
                album_id=kwargs.get('album_id', 0),
                member=request.user,
                )
        for q in queryset:
            q.is_deleted = True
            q.save()
        return Response(status=204)

class MemberPurchasedAlbumViewSet(PodcastAlbumViewSet):
    def get_queryset(self):
        queryset = self.model.objects.filter(
                is_deleted=False,
                status='publish',
                )
        from term.models import Purchase
        member_purchased = Purchase.objects.filter(
                member_id=self.kwargs.get('member_id', 0),
                )
        return queryset
