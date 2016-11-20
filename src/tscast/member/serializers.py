from rest_framework import serializers
from rest_framework.exceptions import NotFound 
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

from .models import PodcastAlbumSubscription
from .models import Member

from podcast.models  import PodcastAlbum

from podcast.serializers import PodcastAlbumSerializer


class PodcastAlbumSubscriptionSerializer(serializers.ModelSerializer):
    # album = serializers.SerializerMethodField()
    album = PodcastAlbumSerializer()

    class Meta:
        model = PodcastAlbumSubscription
        fields = ('album', 'dt_created')

    def get_album(self, instance):
        data = {
            'id': instance.album.id,
            'title': instance.album.title,
            'image': instance.album.image if instance.album.image else None,
            }
        return data

class CurrentMember(object):
    def set_context(self, serializer_field):
        self.member = serializer_field.context['request'].user

    def __call__(self):
        return self.member


class CurrentAlbum(object):
    def set_context(self, serializer_field):
        album_id = serializer_field.context['view'].kwargs.get('album_id', 0)
        try:
            self.album = PodcastAlbum.objects.get(
                    id=album_id,
                    status='publish',
                    )
        except PodcastAlbum.DoesNotExist as error:
            raise NotFound

    def __call__(self):
        return self.album


class PodcastAlbumSubscribeSerializer(serializers.ModelSerializer):
    member = serializers.PrimaryKeyRelatedField(
            read_only=True,
            default=CurrentMember()
            )
    album = serializers.PrimaryKeyRelatedField(
            read_only=True,
            default=CurrentAlbum()
            )
    class Meta:
        model = PodcastAlbumSubscription
        fields = ('member', 'album')


class MemberSerializer(serializers.ModelSerializer):
    expire_datetime = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = ('nickname', 'avatar', 'expire_datetime')

    def get_expire_datetime(self, obj):
        return obj.privilege.expires_datetime
        
