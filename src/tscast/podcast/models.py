from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import get_storage_class
from django.conf import settings

from .managers import BaseManager

def path_join(args):
    return '/'.join(args)

PODCAST_ENCLOSURE_STORAGE= get_storage_class(getattr(settings, 'PODCAST_ENCLOSURE_STORAGE', None))()


PODCAST_IMAGE_STORAGE = get_storage_class(getattr(settings, 'PODCAST_IMAGE_STORAGE', None))()


COPYRIGHT_CHOICES = (
    ('All rights reserved', 'All rights reserved'),
    ('Creative Commons: Attribution (by)', 'Creative Commons: Attribution (by)'),
    ('Creative Commons: Attribution-Share Alike (by-sa)', 'Creative Commons: Attribution-Share Alike (by-sa)'),
    ('Creative Commons: Attribution-No Derivatives (by-nd)', 'Creative Commons: Attribution-No Derivatives (by-nd)'),
    ('Creative Commons: Attribution-Non-Commercial (by-nc)', 'Creative Commons: Attribution-Non-Commercial (by-nc)'),
    ('Creative Commons: Attribution-Non-Commercial-Share Alike (by-nc-sa)', 'Creative Commons: Attribution-Non-Commercial-Share Alike (by-nc-sa)'),
    ('Creative Commons: Attribution-Non-Commercial-No Dreivatives (by-nc-nd)', 'Creative Commons: Attribution-Non-Commercial-No Dreivatives (by-nc-nd)'),
    ('Public domain', 'Public domain'),
)


EXPLICIT_CHOICES = (
    ('yes', _('Explicit Yes')),
    ('no', _('Explicit No')),
    ('clean', _('Explicit Clean')),
)


STATUS_CHOICES = (
    ('draft', _('Draft')),
    ('public', _('Public')),
    ('private', _('Private')),
)


FREQUENCY_CHOICES = (
    # ('always', _('Always')),
    ('unknown', _('Unknown')),
    ('hourly', _('Hourly')),
    ('daily', _('Daily')),
    ('weekly', _('Weekly')),
    ('monthly', _('Monthly')),
    ('yearly', _('Yearly')),
    # ('never', _('Never')),
)


TEXT_TYPE_CHOICES = (
    ('plain', 'Plain text'),
    ('html', 'HTML'),
)


class BaseModel(models.Model):
    desc_type = models.CharField(max_length=32, default='plain', choices=TEXT_TYPE_CHOICES, verbose_name=_('description type'))
    description = models.TextField(blank=True, default='', verbose_name=_('description'))
    slug = models.SlugField(blank=True, unique=True, help_text=_('a URL-friendly name. For example, a slug for "Games & Hobbies" is "games-hobbies".'))
    is_deleted = models.BooleanField(default=False, verbose_name=_('is deleted'))
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name=_('created datetime'))
    dt_updated = models.DateTimeField(auto_now=True, verbose_name=_('updated datetime'))

    objects = BaseManager()

    class Meta:
        abstract = True
        ordering = ['-dt_updated', 'id', 'slug']


# class PodcastOrganization(BaseModel):
#     '''
#     For multiple organizations platform
#     '''
#     name = models.CharField(max_length=32, unique=True, verbose_name=_('organization'))
# 
#     class Meta:
#         app_label = 'podcast'
#         verbose_name = _('podcast organization')
#         verbose_name_plural = _('podcast organizations')
#         get_latest_by = 'dt_updated'
# 
#     def __unicode__(self):
#         return self.name


def podcast_people_image_upload_to(instance, filename):
    args = (
        'podcast',
        'people',
        'image',
        filename,
        )
    return path_join(args)


class PodcastPeople(BaseModel):
    '''
    Podcast People
    '''
    name = models.CharField(max_length=128, verbose_name=_('people name'))
    image = models.ImageField(blank=True, upload_to=podcast_people_image_upload_to, storage=PODCAST_IMAGE_STORAGE, verbose_name=_('image'))

    class Meta:
        app_label = 'podcast'
        verbose_name = _('podcast people')
        verbose_name_plural = _('podcast people')
        get_latest_by = 'dt_updated'
    
    def __unicode__(self):
        return self.name


class PodcastHost(PodcastPeople):
    '''
    Podcast Host
    '''

    class Meta:
        app_label = 'podcast'
        verbose_name = _('podcast host')
        verbose_name_plural = _('podcast hosts')
        get_latest_by = 'dt_updated'


# def podcast_channel_image_upload_to(instance, filename):
#     args = (
#         'podcast',
#         'channel',
#         'image',
#         filename,
#         )
#     return path_join(args)
# 
# class PodcastChannel(BaseModel):
#     '''
#     Podcast Channel
#     '''
#     title = models.CharField(max_length=128, verbose_name=_('channel title'))
#     image = models.ImageField(blank=True, upload_to=podcast_chennel_image_upload_to, storage=PODCAST_IMAGE_STORAGE, verbose_name=_('image'))
# 
#     class Meta:
#         app_label = 'podcast'
#         verbose_name = _('channel')
#         verbose_name_plural = _('channel')
#         get_latest_by = 'dt_updated'
# 
# 
# 
# class PodcastCategory(BaseModel):
#     '''
#     Podcast Content Category
#     '''
#     class Meta:
#         app_label = 'podcast'
#         verbose_name = _('channel')
#         verbose_name_plural = _('channel')
#         get_latest_by = 'dt_updated'


def podcast_album_image_upload_to(instance, filename):
    args = (
        'podcast',
        'album',
        'image',
        filename,
        )
    return path_join(args)

class PodcastAlbum(BaseModel):
    '''
    Podcast Album
    '''
    title = models.CharField(max_length=128, verbose_name=_('album title'))
    image = models.ImageField(blank=True, upload_to=podcast_album_image_upload_to, storage=PODCAST_IMAGE_STORAGE, verbose_name=_('image'))
    keywords = models.CharField(max_length=256, blank=True, default='', verbose_name=_('keywords'))
    hosts = models.ManyToManyField('PodcastHost', related_name='albums', verbose_name=_('hosts'))
    copyright = models.CharField(max_length=256, default='All rights reserved', choices=COPYRIGHT_CHOICES, verbose_name=_('copyright'))
    explicit = models.CharField(max_length=32, default='no', choices=EXPLICIT_CHOICES, verbose_name=_('explicit'))
    frequency = models.CharField(max_length=32, default='unknown', choices= FREQUENCY_CHOICES, verbose_name=_('frequency'))
    status = models.CharField(max_length=32, default='draft', choices=STATUS_CHOICES, verbose_name=_('stauts'))

    class Meta:
        app_label = 'podcast'
        verbose_name = _('podcast album')
        verbose_name_plural = _('podcast albums')
        get_latest_by = 'dt_updated'

    def __unicode__(self):
        return self.title


def podcast_episode_image_upload_to(instance, filename):
    args = (
        'podcast',
        'episode',
        'image',
        filename,
        )
    return path_join(args)

class PodcastEpisode(BaseModel):
    '''
    Podcast Episode
    '''
    album = models.ForeignKey('PodcastAlbum', related_name='episodes', verbose_name=_('album'))
    hosts = models.ManyToManyField('PodcastHost', related_name='episodes', verbose_name=_('hosts'))
    title = models.CharField(max_length=128, verbose_name=_('episode title'))
    image = models.ImageField(blank=True, upload_to=podcast_episode_image_upload_to, storage=PODCAST_IMAGE_STORAGE, verbose_name=_('image'))
    keywords = models.CharField(max_length=256, blank=True, default='', verbose_name=_('keywords'))
    copyright = models.CharField(max_length=256, default='All rights reserved', choices=COPYRIGHT_CHOICES, verbose_name=_('copyright'))
    explicit = models.CharField(max_length=32, default='no', choices=EXPLICIT_CHOICES, verbose_name=_('explicit'))
    status = models.CharField(max_length=32, default='draft', choices=STATUS_CHOICES, verbose_name=_('stauts'))

    class Meta:
        app_label = 'podcast'
        verbose_name = _('podcast episode')
        verbose_name_plural = _('podcast episodes')
        get_latest_by = 'dt_updated'

    def __unicode__(self):
        return self.title


def podcast_enclosure_upload_to(instance, filename):
    args = (
        'podcast',
        'enclosure',
        filename,
        )
    return path_join(args)

class PodcastEnclosure(BaseModel):
    '''
    Podcase Enclosure Model
    '''

    EXPRESSION_CHOICES = (
        ('preview', _('Preview')),
        ('full', _('Full')),
    )

    slug = None
    episode = models.ForeignKey(PodcastEpisode, related_name='enclosures', verbose_name=_('episode'))
    title = models.CharField(max_length=255, blank=True, verbose_name=_('title'))
    expression = models.CharField(max_length=32, default='full', choices=EXPRESSION_CHOICES, verbose_name=_('expression'))
    file = models.FileField(upload_to=podcast_enclosure_upload_to, storage=PODCAST_ENCLOSURE_STORAGE, verbose_name=_('file'))
    hash = models.CharField(max_length=255, blank=True)
    length = models.IntegerField(blank=True, default=0,  verbose_name=_('length'))
    size = models.IntegerField(blank=True, default=0, verbose_name=_('file size'))

    class Meta:
        app_label = 'podcast'
        verbose_name = _('podcast enclosure')
        verbose_name_plural = _('podcast enclosures')
        get_latest_by = 'dt_updated'

    def __unicode__(self):
        return self.file.name