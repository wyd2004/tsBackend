from __future__ import unicode_literals
import uuid

from django.utils.translation import ugettext_lazy as _
from django.db import models

from rest_framework.authtoken.models import Token


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
    user = models.ForeignKey('Member', related_name='tokens', on_delete=models.CASCADE, verbose_name=_('user'))
    key = models.CharField(max_length=40, primary_key=True, verbose_name=_('token'))

    class Meta:
        app_label = 'member'
        verbose_name = _('member token')
        verbose_name_plural = _('member tokens')

    def __unicode__(self):
        uname = '%s: %s' % (self.user.username, self.key)
        return uname


class Member(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name=_('uuid'))
    username = models.CharField(max_length=32, unique=True, verbose_name=_('username'))
    nickname = models.CharField(max_length=32, null=True, unique=True, verbose_name=_('nickname'))
    avatar = models.ImageField(blank=True, verbose_name=_('avatar'))

    class Meta:
        app_label = 'member'
        verbose_name = _('member')
        verbose_name_plural = _('members')

    def __unicode__(self):
        return self.username


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
        uname = '%s: %s' % (self.member.username, slf.album.name)
        return uname
