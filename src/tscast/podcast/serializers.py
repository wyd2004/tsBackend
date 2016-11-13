from rest_framework import serializers
from rest_framework.exceptions import NotFound 
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

from .models import PodcastHost
from .models import PodcastAlbum
from .models import PodcastEpisode
from .models import PodcastEnclosure


class PodcastHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastHost
        fields = ('id', 'name', 'description', 'image')


class PodcastAlbumSerializer(serializers.ModelSerializer):
    hosts = PodcastHostSerializer(many=True)
    is_new = serializers.SerializerMethodField()
    latest_update = serializers.SerializerMethodField()
    episodes_count = serializers.SerializerMethodField()

    class Meta:
        model = PodcastAlbum
        fields = ('id', 'title', 'image', 'description',
                'keywords', 'copyright', 'explicit',
                'frequency', 'hosts', 'is_new',
                'latest_update', 'episodes_count')

    def get_is_new(self, instance):
        return False

    def get_latest_update(self, instance):
        last = instance.episodes.filter(
                status='publish',
                is_deleted=False,
                )
        if last:
            last = last.latest('dt_updated')
        return last.dt_updated if last else None

    def get_episodes_count(self, instance):
        return instance.episodes.filter(
                status='publish',
                is_deleted=False,
                ).count()


class PodcastEpisodeSerializer(serializers.ModelSerializer):
    hosts = PodcastHostSerializer(many=True)
    enclosures = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    album_title = serializers.SerializerMethodField()


    class Meta:
        model = PodcastEpisode
        fields = ('id', 'album_title', 'serial', 'title',
                'subtitle', 'image', 'description', 'length',
                'keywords', 'copyright', 'explicit',
                'hosts', 'enclosures', 'price', 'dt_updated',
                )
    
    def get_album_title(self, instance):
        return instance.album.title

    def get_price(self, instance):
        return 0

    def get_enclosures(self, instance):
        previews = instance.enclosures.filter(expression='preview')
        fulls = instance.enclosures.filter(expression='full')
        data = {
            'previews': PodcastEnclosureSerializer(previews, many=True).data,
            'fulls': PodcastEnclosureSerializer(fulls, many=True).data
            }
        return data


class PodcastEnclosureSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = PodcastEnclosure
        fields = ('title', 'url', 'length', 'size')

    def get_url(self, instance):
        return instance.file.url if instance.file else None
