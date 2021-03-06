import datetime

import pytz
from rest_framework import serializers
from rest_framework.exceptions import NotFound 
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

from tscast import settings
from .models import PodcastHost
from .models import PodcastAlbum
from .models import PodcastEpisode
# from .models import PodcastEnclosure

from member.models import Member, PodcastAlbumSubscription
from term.models import Tier


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
    # enclosures = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    album_title = serializers.SerializerMethodField()
    full_url = serializers.SerializerMethodField()
    full_length = serializers.SerializerMethodField()
    preview_url = serializers.SerializerMethodField()
    preview_length = serializers.SerializerMethodField()
    privilege = serializers.SerializerMethodField()
    album_id = serializers.SerializerMethodField()
    next_ep_id = serializers.SerializerMethodField()
    previous_ep_id = serializers.SerializerMethodField()
    is_album_sub = serializers.SerializerMethodField()


    class Meta:
        model = PodcastEpisode
        fields = ('id', 'album_title', 'serial', 'title',
                'subtitle', 'image', 'description',
                'keywords', 'copyright', 'explicit',
                'hosts', 'price', 'dt_updated', 'full_url',
                'full_length', 'preview_url', 'preview_length',
                'privilege','album_id','next_ep_id','previous_ep_id',
                'is_album_sub',
                )
    
    def get_album_title(self, instance):
        return instance.album.title

    def get_album_id(self, instance):
        return instance.album.id

    def get_next_ep_id(self, instance):
        all_esp = PodcastEpisode.objects.all().order_by('id')
        ids = []
        for e in all_esp:
            ids.append(e.id)
        cur_index = ids.index(instance.id, 0, len(ids))
        if cur_index >= len(ids) -1:
            return ids[cur_index]
        else:
            return ids[cur_index+1]

    def get_previous_ep_id(self, instance):
        all_esp = PodcastEpisode.objects.all().order_by('id')
        ids = []
        for e in all_esp:
            ids.append(e.id)
        cur_index = ids.index(instance.id, 0, len(ids))
        if cur_index <= 0:
            return ids[cur_index]
        else:
            return ids[cur_index - 1]

    def get_is_album_sub(self, instance):
        is_sub = PodcastAlbumSubscription.objects.filter(
                album=PodcastAlbum.objects.filter(id=instance.album.id),
                member=self.context['request'].user,
                is_deleted=False).exists()
        if is_sub:
            return True
        else:
            return False

    def get_price(self, instance):
        try:
            esp = PodcastEpisode.objects.get(id=instance.id )
            return esp.price
        except Tier.DoesNotExist as error:
            return 0

    def get_full_url(self, instance):
        if self.context.get('request'):
            host = self.context['request'].META.get('HTTP_HOST')
            host = 'http://%s' % host
        else:
            host = ''
        uri = '/podcast/episode/%d/full_file/' % instance.id

        if self.context.get('request'):
            request = self.context['request']
            if type(request.user) is Member:
                privilege = request.user.privilege
                if any((
                        (instance.id in privilege.episode_ids),
                        (instance.album.id in privilege.album_ids),
                        (instance.album.channel.id in privilege.channel_ids),
                )):
                    tz = pytz.timezone(settings.TIME_ZONE)
                    dt = datetime.datetime.now(tz=tz)
                    tdelta = privilege.expires_datetime - dt
                    if (tdelta.days > 0):
                        if instance.full_file:
                            url = instance.full_file.url
                        else:
                            url = instance.full_file_url
                        return url
        else:
            pass
        return ''

    def get_full_length(self, instance):
        return instance.full_file_length

    def get_preview_url(self, instance):
        if self.context.get('request'):
            host = self.context['request'].META.get('HTTP_HOST')
            host = 'http://%s' % host
        else:
            host = ''
        uri = '/podcast/episode/%d/preview_file/' % instance.id
        url = '%s%s' % (host, uri)

        if instance.preview_file:
            url = instance.preview_file.url
        else:
            url = instance.preview_file_url
        return url

    def get_preview_length(self, instance):
        return instance.full_file_length

    def get_privilege(self, instance):
        if self.context.get('request'):
            request = self.context['request']
            if type(request.user) is Member:
                privilege = request.user.privilege
                if any((
                        (instance.id in privilege.episode_ids),
                        (instance.album.id in privilege.album_ids),
                        (instance.album.channel.id in privilege.channel_ids),
                        )):
                    return ['full', 'preview']
        return ['preview']

    # def get_enclosures(self, instance):
    #     previews = instance.enclosures.filter(expression='preview')
    #     fulls = instance.enclosures.filter(expression='full')
    #     data = {
    #         'previews': PodcastEnclosureSerializer(previews, many=True).data,
    #         'fulls': PodcastEnclosureSerializer(fulls, many=True).data
    #         }
    #     return data


# class PodcastEnclosureSerializer(serializers.ModelSerializer):
#     url = serializers.SerializerMethodField()
# 
#     class Meta:
#         model = PodcastEnclosure
#         fields = ('title', 'url', 'length', 'size')
# 
#     def get_url(self, instance):
#         return instance.file.url if instance.file else None
