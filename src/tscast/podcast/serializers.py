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
    class Meta:
        model = PodcastAlbum
        fields = ('id', 'title', 'image', 'description',
                'slug', 'keywords', 'copyright', 'explicit',
                'frequency', 'hosts')


class PodcastEpisodeSerializer(serializers.ModelSerializer):
    hosts = PodcastHostSerializer(many=True)
    enclosures = serializers.SerializerMethodField()

    class Meta:
        model = PodcastEpisode
        fields = ('id', 'title', 'image', 'description',
                'slug', 'keywords', 'copyright', 'explicit',
                'hosts', 'enclosures')

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
