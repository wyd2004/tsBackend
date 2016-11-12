from __future__ import unicode_literals

import uuid
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models




class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False, verbose_name=_('is deleted'))
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name=_('created datetime'))
    dt_updated = models.DateTimeField(auto_now=True, verbose_name=_('updated datetime'))

    class Meta:
        abstract = True

    def delete(self):
        self.is_deleted = True
        self.save()



# class Tier(BaseModel):
#     code = models.CharField(max_length=32, unique=True, verbose_name=_('tier code'))
#     name = models.CharField(max_length=32, unique=True, verbose_name=_('tier name'))
# 
#     class Meta:
#         app_label = 'term'
#         verbose_name = _('tier')
#         verbose_name_plural = _('tiers')
# 
#     def __unicode__(self):
#         return self.name
# 
# 
# class Scope(BaseModel):
#     code = models.CharField(max_length=32, unique=True, verbose_name=_('tier code'))
#     name = models.CharField(max_length=32, unique=True, verbose_name=_('tier name'))
# 
#     class Meta:
#         app_label = 'term'
#         verbose_name = _('scope')
#         verbose_name_plural = _('scopes')
# 
#     def __unicode__(self):
#         return self.name

TIER_SCOPE_CHOICES = (
        ('yearly', _('Yearly')),
        ('seasonally', _('Seasonally')),
        ('monthly', _('Monthly')),
        ('single', _('Single')),
        )

TIER_PACKAGE_CHOICES = (
        ('channel', _('Channel')),
        ('album', _('Album')),
        ('episode', _('Episode')),
        )

class Tier(BaseModel):
    scope = models.CharField(max_length=32, choices=TIER_SCOPE_CHOICES, verbose_name=_('tier scope'))
    package = models.CharField(max_length=32, choices=TIER_PACKAGE_CHOICES, verbose_name=_('tier package'))
    price = models.DecimalField(decimal_places=2, max_digits=9, default=0.0, verbose_name=_('tier price'))
    is_published = models.BooleanField(default=False, verbose_name=_('is published'))

    class Meta:
        app_label = 'term'
        verbose_name = _('tier')
        verbose_name_plural = _('tiers')

    def __unicode__(self):
        return '%s x %s, %s' % (self.scope, self.package, self.price)


ORDER_STATUS_CHOICES = (
        ('waiting_purchase', _('Waiting purchase')),
        ('succeeded', _('Succeeded')),
        ('failed', _('Faield')),
        )

class Order(BaseModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('uuid'))
    scope = models.CharField(max_length=32, choices=TIER_SCOPE_CHOICES, verbose_name=_('tier scope'))
    package = models.CharField(max_length=32, choices=TIER_PACKAGE_CHOICES, verbose_name=_('tier package'))
    price = models.DecimalField(decimal_places=2, max_digits=9, default=0.0, verbose_name=_('tier price'))
    member = models.ForeignKey('member.Member', related_name='orders', verbose_name = _('member'))
    value = models.DecimalField(decimal_places=2, max_digits=9, default=0.0, verbose_name=_('payment value'))
    status = models.CharField(max_length=32, choices=ORDER_STATUS_CHOICES, verbose_name=_('status'))

    class Meta:
        app_label = 'term'
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __unicode__(self):
        return '%s: %s' % (self.uuid, self.status)


PAYMENT_AGENT_CHOICES = (
        ('wechat', _('Wechat')),
        )


PAYMENT_STATUS_CHOICES = (
        ('waiting_purchase', _('Waiting purchase')),
        ('succeeded', _('Succeeded')),
        ('failed', _('Faield')),
        )

class Payment(BaseModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('uuid'))
    order = models.ForeignKey('Order', related_name='payments', verbose_name=_('payment'), editable=False)
    receipt = models.TextField(blank=True, verbose_name=_('payment receipt'), editable=False)
    agent = models.CharField(max_length=32, choices=PAYMENT_AGENT_CHOICES, verbose_name=_('payment agent'), editable=False)
    status = models.CharField(max_length=32, choices=PAYMENT_STATUS_CHOICES, verbose_name=_('status'))

    class Meta:
        app_label = 'term'
        verbose_name = _('payment')
        verbose_name_plural = _('payments')

    def __unicode__(self):
        return '%s: %s' % (self.uuid, self.status)


TICKET_CONTENT_TYPE_LIMITS = (
        models.Q(name='PodcastChannel', label='podcast')
        | models.Q(name='PodcastAlbum', label='podcast')
        | models.Q(name='PodcastEpisode', label='podcast')
        )

class Ticket(BaseModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('uuid'))
    scope = models.CharField(max_length=32, choices=TIER_SCOPE_CHOICES, verbose_name=_('tier scope'))
    package = models.CharField(max_length=32, choices=TIER_PACKAGE_CHOICES, verbose_name=_('tier package'))
    price = models.DecimalField(decimal_places=2, max_digits=9, default=0.0, verbose_name=_('tier price'))
    content_type = models.ForeignKey('contenttypes.ContentType', null=True, blank=True, verbose_name=_('content_type'), limit_choices_to=TICKET_CONTENT_TYPE_LIMITS)
    object_id = models.PositiveIntegerField(verbose_name=_('object id'), default=0)
    ticket_object = GenericForeignKey('content_type', 'object_id')
    order = models.ForeignKey('Order', related_name='tickets', verbose_name=_('order'))
    member = models.ForeignKey('member.Member', related_name='tickets', verbose_name=_('member'))

    class Meta:
        app_label = 'term'
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')

    def __unicode__(self):
        return self.uuid
