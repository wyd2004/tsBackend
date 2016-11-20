from __future__ import unicode_literals

import json
import uuid

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.timezone import now
from django.utils.dateparse import parse_datetime

from rest_framework.authtoken.models import Token

from .signals import update_member_privilege


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False, verbose_name=_('is deleted'))
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name=_('created datetime'))
    dt_updated = models.DateTimeField(auto_now=True, verbose_name=_('updated datetime'))

    class Meta:
        abstract = True

    def delete(self):
        self.is_deleted = True
        self.save()


class MemberToken(models.Model):
    user = models.ForeignKey('Member', related_name='tokens', on_delete=models.CASCADE, verbose_name=_('member'))
    key = models.CharField(max_length=40, primary_key=True, verbose_name=_('token'))

    class Meta:
        app_label = 'member'
        verbose_name = _('member token')
        verbose_name_plural = _('member tokens')

    def __unicode__(self):
        uname = '%s: %s' % (self.user.username, self.key)
        return uname


class Member(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name=_('uuid'))
    username = models.CharField(max_length=32, unique=True, verbose_name=_('username'))
    nickname = models.CharField(max_length=32, null=True, unique=True, verbose_name=_('nickname'))
    avatar = models.ImageField(blank=True, verbose_name=_('avatar'))

    class Meta:
        app_label = 'member'
        verbose_name = _('member')
        verbose_name_plural = _('members')

    def __unicode__(self):
        return self.username

    @property
    def privilege(self):
        try:
            mp = self.memberprivilege
        except Exception as error:
            mp, created = MemberPrivilege.objects.get_or_create(member=self)
        _privilege = Privilege()
        _privilege.loads(mp.payload)
        return _privilege


SOCIAL_NETWORK_SITE_CHOICES = (
        ('unknown', _('Unknown')),
        ('wechat', _('Wechat')),
        )

class SocialNetwork(models.Model):
    member = models.ForeignKey('Member', related_name='social_networks', verbose_name=_('member'))
    site = models.CharField(max_length=32, choices=SOCIAL_NETWORK_SITE_CHOICES, verbose_name=_('sns'))
    identifier = models.CharField(max_length=128, unique=True, verbose_name=_('identifier'))
    nickname = models.CharField(max_length=32, verbose_name=_('nickname'))
    avatar = models.ImageField(blank=True, verbose_name=_('avatar'))

    class Meta:
        app_label = 'member'
        verbose_name = _('social network')
        verbose_name_plural = _('social networks')

    def __unicode__(self):
        uname = '%s %s' % (self.site, self.identifier)
        return uname


class PodcastAlbumSubscription(BaseModel):
    member = models.ForeignKey('Member', related_name='album_subscriptions', verbose_name=_('member'))
    album = models.ForeignKey('podcast.PodcastAlbum', related_name='member_subscriptions', verbose_name=_('album'))

    class Meta:
        app_label = 'member'
        verbose_name = _('podcast album subscription')
        verbose_name_plural = _('podcast album subscriptions')
    
    def __unicode__(self):
        uname = '%s: %s' % (self.member.username, self.album.title)
        return uname


class MemberPrivilege(BaseModel):
    member = models.OneToOneField(Member, verbose_name=_('member'))
    payload = models.TextField(blank=True, verbose_name=_('payload'))

    class Meta:
        app_label = 'member'
        verbose_name = _('member privilege')
        verbose_name_plural = _('member privileges')

    def __unicode__(self):
        return '%s - privilege' % self.member.username


class Privilege(object):
    expires_datetime = None
    channels = None
    albums = None
    episodes = None
    channel_ids = None
    album_ids = None
    episode_ids = None
    is_dirty = True
     
    def __init__(self, purchase_queryset=None):
        self.expires_datetime = now() # TODO
        self.channels = []
        self.albums = []
        self.episodes = []
        self.channel_ids = set()
        self.album_ids = set()
        self.episode_ids = set()
        if purchase_queryset:
            for package, payload in self.make_payload(
                    purchase_queryset):
                if package == 'channel':
                    self.channels.append(payload)
                elif package == 'album':
                    self.albums.append(payload)
                elif package == 'episode':
                    self.episodes.append(payload)
        self.is_dirty = False

    def make_payload(self, purchase_queryset):
        for purchase in purchase_queryset:
            purchase_object = purchase.purchase_object
            payload = {
                    'dt_created': purchase.dt_created,
                    'dt_expired': purchase.dt_expired,
                    'is_permanent': purchase.is_permanent,
                    'object_id': purchase.object_id,
                    'channel': None,
                    'album': None,
                    'episode': None,
                    }
            if purchase.content_type.model == 'podcastchannel':
                payload['channel'] = purchase_object.id
                payload['album'] = '__all__'
                payload['episode'] = '__all__'
                self.channel_ids.add(payload['channel'])
            elif purchase.content_type.model == 'podcastalbum':
                payload['channel'] = purchase_object.channel_id
                payload['album'] = purchase_object.id
                payload['episode'] = '__all__'
                self.channel_ids.add(payload['channel'])
                self.album_ids.add(payload['album'])
            elif purchase.content_type.model == 'podcastepisode':
                payload['channel'] = purchase_object.album.channel_id
                payload['album'] = purchase_object.album_id
                payload['episode'] = purchase_object.id
                self.channel_ids.add(payload['channel'])
                self.album_ids.add(payload['album'])
                self.episode_ids.add(payload['episode'])
            yield purchase.package, payload

    def dumps(self):
        data = {
                'expires_datetime': self.expires_datetime,
                'channels': self.channels,
                'albums': self.albums,
                'episodes': self.episodes,
                'channel_ids': list(self.channel_ids),
                'album_ids': list(self.album_ids),
                'episode_ids': list(self.episode_ids),
                }
        return json.dumps(data, cls=DjangoJSONEncoder)

    def loads(self, json_data):
        if not json_data:
            return
        try:
            data = json.loads(json_data)
            self.expires_datetime = parse_datetime(data['expires_datetime'])
            self.channel = data['channels']
            self.album = data['albums']
            self.episode = data['episodes']
            self.channel_ids = data['channel_ids']
            self.album_ids = data['album_ids']
            self.episode_ids = data['episode_ids']
            self.is_dirty = False
        except Exception as error:
            self.is_dirty = True
